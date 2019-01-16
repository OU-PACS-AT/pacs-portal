# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.shortcuts import redirect

from scaffold.forms import CourseSimpleSearch
from apitools.models import CanvasAssignment
from apitools.models import CanvasClass
from apitools.models import CanvasStudent
# User Credentials retrieval/mixins
from nucleus.mixins import CurrentUserMixin

from toolkit.views import CCECreateView, CCECreateWithInlinesView, CCEDeleteView, CCEDetailView, \
    CCEFormView, CCEListView, CCEModelFormSetView, CCEObjectRedirectView, CCERedirectView, \
    CCESearchView, CCETemplateView, CCEUpdateView,  CCEUpdateWithInlinesView, \
    ReportDownloadDetailView, ReportDownloadSearchView

from nucleus.auth import UserCredentials
from faculty_tools.api import CanvasAPI

from datetime import datetime, timedelta, tzinfo, date, time

from apitools.forms import TableFormSet
from apitools.forms import XTableFormSet

import logging
import requests

class CanvasSearchView(CCESearchView):
    def __init__(self, *args, **kwargs):
        super(CanvasSearchView, self).__init__(*args, **kwargs)
        from nucleus.auth import UserCredentials
        creds = UserCredentials()
        self.model.objects.filter(created_by = creds.get_OUNetID()).delete()
   
class CanvasListView(CCEListView):
    def __init__(self, *args, **kwargs):
        super(CanvasListView, self).__init__(*args, **kwargs)
        from nucleus.auth import UserCredentials
        creds = UserCredentials()
        self.model.objects.filter(created_by = creds.get_OUNetID()).delete()
        
class CanvasUpdateView(CCEUpdateView):
    def __init__(self, *args, **kwargs):
        super(CanvasUpdateView, self).__init__(*args, **kwargs)
        from nucleus.auth import UserCredentials
        creds = UserCredentials()
        self.model.objects.filter(created_by = creds.get_OUNetID()).delete()

class CanvasModelFormSetView(CCEModelFormSetView):
    def __init__(self, *args, **kwargs):
        super(CanvasModelFormSetView, self).__init__(*args, **kwargs)
        from nucleus.auth import UserCredentials
        creds = UserCredentials()
        self.model.objects.filter(created_by = creds.get_OUNetID()).delete()
        
class CanvasFormView(CCEFormView):
    def __init__(self, *args, **kwargs):
        super(CanvasFormView, self).__init__(*args, **kwargs)
        from nucleus.auth import UserCredentials
        creds = UserCredentials()
        self.model.objects.filter(created_by = creds.get_OUNetID()).delete()


class CourseListView(CurrentUserMixin, CanvasSearchView):
    model = CanvasClass
    page_title = 'Change Dates Course Selection'
    search_form_class = CourseSimpleSearch
    success_message = "success"
    sidebar_group = ['faculty_tools', 'course_lists']
    columns = [
        ('Course ID', 'class_number'),
        ('Name', 'class_name'),
        ('Created at', 'created_at'),
        ('Created by', 'created_by'),
    ]
    paginate_by = 5
    show_context_menu = False
    
    def __init__(self, *args, **kwargs):
        """
            Needs to get list of courses attached to logged in user and store
            in database
        """
        super(CourseListView, self).__init__(*args, **kwargs)        
        creds = UserCredentials()
        api = CanvasAPI()
        api_response = api.getCanvasID(creds.get_OUNetID())        
        api_list = list(api_response)
        for c in api_list:
            canvasID = c['id']
            #logging.warning ('canvasID*******************' +str(canvasID) + '*********************canvasID')

        api_response = api.get_class_by_teacher(canvasID)
        api_list = list(api_response)
        for course in api_list:
            course_id = course['id']
            course_name = course['name']
            course_create = CanvasClass.objects.create(class_number = course_id, class_name = course_name, last_updated_by = creds.get_OUNetID(), created_by = creds.get_OUNetID() )   

    def get_queryset(self):
        creds = UserCredentials()
        return super(CourseListView, self).get_queryset()\
            .filter(created_by = creds.get_OUNetID())


    def render_buttons(self, user, obj, *args, **kwargs):
        import requests
        buttons = super(CourseListView, self).render_buttons(user, obj,
                                                            *args, **kwargs)
        buttons.append(

            self.render_button(btn_class='btn-edit',
                               button_text='Edit Assignment Dates',
                               icon_classes='glyphicon glyphicon-edit',
                               url=reverse('course_lists') + str(obj.class_number) + "/edit/",)
        )
        
        #buttons.append(
        #    self.render_button(btn_class='btn-edit',
        #                       button_text='Extend Assignment Dates',
        #                       icon_classes='glyphicon glyphicon-edit',
        #                       url=reverse('course_lists') + str(obj.class_number) + "/extend/",)
        #)
        
        return buttons


class OrderException(Exception):
    pass

class changeDates(CurrentUserMixin, CCETemplateView):
        
    model = CanvasAssignment
    page_title = 'Change Dates'
    success_message = "success"
    add_button_title = "add_button"
    form = TableFormSet
    template_name = "canvasassignment_list.html"
    sidebar_group = ['faculty_tools', 'changeDates']
    columns = [
        ('Assignment #', 'assignment_number'),
        ('Assignment Name', 'assignment_name'),
        ('Start Date', 'start_date'),
        ('Due Date', 'due_date'),
        ('End Date', 'end_date'),
        ]
    
    fields = [
        'assignment_name',
        'start_date',
        'due_date',
        'end_date',
        ]
        
    
    paginate_by = 100
    show_context_menu = False
    
    def get(self, request, course_id, *args, **kwargs):
        logging.warning("course_id: " + str(course_id))
        
        request.session['course_id'] = course_id
        #course = CanvasClass.objects.filter(class_number = request.session.get('course_id'))
        #className = course.class_name
        creds = UserCredentials()
        api = CanvasAPI()
        
        json_data = api.get_assignments(course_id)            
            
        logging.warning("json_data" + str(json_data))
        json_list = list(json_data) #the data from canvas
        for assignment in json_list:   #get the stuff i need from the canvas data             
            assignment_number = assignment['id']
            assignment_name = assignment['name']                
            td = timedelta (hours = 6)#adjust to local time      
            if assignment['unlock_at'] is not None:
                unlockCanvas = datetime.strptime(assignment['unlock_at'], '%Y-%m-%dT%H:%M:%SZ')#save in datetime object
                unlockCanvas = unlockCanvas - td#adjust time.  else it goes past midnight altering the date
                start_date = datetime.strftime(unlockCanvas, '%m/%d/%Y')#remove time and save just the date as a string
            else:
                start_date = None
            if assignment['due_at'] is not None:
                dueCanvas = datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ')
                dueCanvas = dueCanvas - td
                due_date = datetime.strftime(dueCanvas, '%m/%d/%Y')#saving date as string and in m/d/y for use with datepicker
            else:
                due_date = None
            if assignment['lock_at'] is not None:
                lockCanvas = datetime.strptime(assignment['lock_at'], '%Y-%m-%dT%H:%M:%SZ')                
                lockCanvas = lockCanvas - td 
                end_date = datetime.strftime(lockCanvas, '%m/%d/%Y')
            else:
                end_date = None
                                
            newAssignment = CanvasAssignment.objects.create(assignment_number = assignment_number, assignment_name = assignment_name, start_date = start_date, due_date = due_date, end_date = end_date, class_number = course_id , created_by = creds.get_OUNetID(), last_updated_by = creds.get_OUNetID())
            #newAssignment = Assignment.objects.create(assignment_number = assignment['id'], assignment_name = assignment['name'] , start_date = assignment['unlock_at'], due_date = assignment['due_at'], end_date = assignment['lock_at'], course_id = course_id, created_by = creds.get_OUNetID(), last_updated_by = creds.get_OUNetID())
        
        form = TableFormSet (queryset = CanvasAssignment.objects.filter(created_by = creds.get_OUNetID()))
        sup = super(changeDates, self).get(request, *args, **kwargs)
        args = {'form' : form, 'sup' : sup}
        return render(request, self.template_name, args)  
    
         
    def post(self, request, course_id, *args, **kwargs):
        if request.POST.get("Save Dates Button"):#save updated dates back to canvas 
            course_id = request.session.get('course_id')                      
            table = TableFormSet(request.POST)  
            capi = CanvasAPI() 
            creds = UserCredentials()
            tableErorr = ""
            
            if table.is_valid():
                #logging.warning ('TABLEVALID****************************************TABLEVALID')
                table.save()            
                
            assignments = CanvasAssignment.objects.filter(class_number = request.session.get('course_id'))#get string dates from local db
                        
            for assignment in assignments:#need to rebuild date object to send to canvas

                starttime = time(0,0,0)#time object
                endtime = time(23,59,00)                
                
                unlockDate = datetime.strptime(assignment.start_date, '%m/%d/%Y').date()#make date object from date string
                dueDate = datetime.strptime(assignment.due_date, '%m/%d/%Y').date()
                endDate = datetime.strptime(assignment.end_date, '%m/%d/%Y').date()
                    
                if unlockDate > dueDate:# will get HTTPError at / 400 Client Error: Bad Request if the dates are out of order
                    raise OrderException('Some of the dates are out of order.  The Start Date must be before the Due Date.')                    
                if dueDate > endDate:
                    raise OrderException('Some of the dates are out of order.  The Due Date must be before the End Date.')
                
                unlockDateTime = datetime.combine(unlockDate,starttime)#make datetime object by combining date and time
                dueDateTime = datetime.combine(dueDate,endtime)
                endDateTime = datetime.combine(endDate,endtime)
                
                unlock_at = unlockDateTime.isoformat()#canvas uses iso format
                due_at = dueDateTime.isoformat()                
                lock_at = endDateTime.isoformat() 
                
                id = assignment.assignment_number#building payload for api put()
                url = "/courses/" + str(course_id) + "/assignments/" 
                url = url + str(id)
                payload = {'assignment[due_at]':due_at, 'assignment[unlock_at]':unlock_at, 'assignment[lock_at]':lock_at}               
                capi.put(url, payload)#canvas api has no group assignment call.  so makes a seperate call for each assignemnt
                    
            #end for assignment in assignments
                
            request.session['course_id'] = 0
            CanvasAssignment.objects.filter(created_by = creds.get_OUNetID()).delete()
            return  redirect('course_lists')
        #end if (save dates button)
        if request.POST.get("Quit"):
            creds = UserCredentials()
            request.session['course_id'] = 0
            CanvasAssignment.objects.filter(created_by = creds.get_OUNetID()).delete()
            return  redirect('course_lists')
        #end if quit
    #end change dates
    