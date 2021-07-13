# Django Core
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

# Nucleus imports 
from nucleus.mixins import CurrentUserMixin
from nucleus.auth import UserCredentials
from nucleus.api import CanvasAPI
from nucleus import settings

# Library imports
from datetime import datetime, timedelta, tzinfo, date, time
import logging
import requests
import csv

# Toolkit views
from toolkit.views import CCECreateView, CCECreateWithInlinesView, CCEDeleteView, CCEDetailView, \
    CCEFormView, CCEListView, CCEModelFormSetView, CCEObjectRedirectView, CCERedirectView, \
    CCESearchView, CCETemplateView, CCEUpdateView,  CCEUpdateWithInlinesView, \
    ReportDownloadDetailView, ReportDownloadSearchView

# Form imports
from forms import CourseSimpleSearchForm, CourseAdvancedSearchForm, TermSimpleSearchForm, SubaccountSimpleSearchForm
from forms import AssignmentSimpleSearchForm, AssignmentAdvancedSearchForm
from forms import UserSimpleSearchForm, UserCourseSimpleSearchForm, UserCourseAdvancedSearchForm 
from forms import TeacherWeeklyReportSimpleSearchForm
from models import Course, Term, Subaccount, User, UserCourse
from models import TeacherWeeklyReport, TeacherWeeklyReportDiscussions, TeacherWeeklyReportAssignments
from faculty_tools.models import Assignment

class CourseListView(CurrentUserMixin, CCESearchView):
    model = Course
    page_title = 'Course List'
    search_form_class = CourseSimpleSearchForm
    advanced_search_form_class = CourseAdvancedSearchForm
    sidebar_group = ['faculty_tools', 'canvas_course_list']
    columns = [
        ('Course ID', 'course_id'),
        ('Name', 'name'),
        ('Course Code', 'course_code'),
        ('Subaccount', 'subaccount'),
        ('Term', 'term')
    ]
    paginate_by = 50
    
    def render_buttons(self, user, obj, *args, **kwargs):
        buttons = super(CourseListView, self).render_buttons(user, obj,
                                                            *args, **kwargs)
        
        buttons.append(
            self.render_button(btn_class='btn-warning btn-inline',
                               button_text='View Submissions',
                               icon_classes='glyphicon glyphicon-paste',
                               url= "/ft/canvas_course_list/" + str(obj.course_id) + "/submissions/",
                               label="View Submissions",
                               condensed=False,)
        )
        
        return buttons
    
class AdminCourseListView(CurrentUserMixin, CCESearchView):
    model = Course
    page_title = 'Admin Course List'
    search_form_class = CourseSimpleSearchForm
    advanced_search_form_class = CourseAdvancedSearchForm
    sidebar_group = ['canvas', 'canvas_admincourse_list']
    columns = [
        ('Course ID', 'course_id'),
        ('Name', 'name'),
        ('Course Code', 'course_code'),
        ('Subaccount', 'subaccount'),
        ('Term', 'term')
    ]
    paginate_by = 50
    
    def render_buttons(self, user, obj, *args, **kwargs):
        buttons = super(AdminCourseListView, self).render_buttons(user, obj,
                                                            *args, **kwargs)
        
        buttons.append(
            self.render_button(btn_class='btn-warning btn-inline',
                               button_text='View Users',
                               icon_classes='fas fa-user-graduate',
                               url= "/c/usercourse/" + str(obj.course_id) + "/",
                               label="View Users",
                               condensed=False,)
        )
        
        buttons.append(
            self.render_button(btn_class='btn-warning btn-inline',
                               button_text='View Assignments',
                               icon_classes='fas fa-book-open',
                               url= "/c/assignment/" + str(obj.course_id) + "/",
                               label="View Assignments",
                               condensed=False,)
        )
        
        buttons.append(
            self.render_button(btn_class='btn-warning btn-inline',
                               button_text='View Submissions',
                               icon_classes='glyphicon glyphicon-paste',
                               url= "/ft/canvas_course_list/" + str(obj.course_id) + "/submissions/",
                               label="View Submissions",
                               condensed=False,)
        )
        
        return buttons
    
class UserListView(CurrentUserMixin, CCESearchView):
    model = User
    page_title = 'Canvas User List'
    search_form_class = UserSimpleSearchForm
    sidebar_group = ['canvas', 'canvas_user_list']
    columns = [
        ('Name', 'sortable_name'),
        ('Login ID', 'login_id'),        
        ('Canvas ID', 'canvas_id'),
        ('SIS ID', 'sis_user_id'),
    ]
    paginate_by = 50
    
class TermListView(CurrentUserMixin, CCESearchView):
    model = Term
    page_title = 'Term List'
    search_form_class = TermSimpleSearchForm
    sidebar_group = ['canvas', 'canvas_term_list']
    columns = [
        ('Term ID', 'term_id'),    
        ('Name', 'name'),
    ]
    paginate_by = 50
    
    def get_queryset(self, *args, **kwargs):
        return super(TermListView,self).get_queryset().order_by('term_id','name')
    
class SubaccountListView(CurrentUserMixin, CCESearchView):
    model = Subaccount
    page_title = 'Subaccount List'
    search_form_class = SubaccountSimpleSearchForm
    sidebar_group = ['canvas', 'canvas_subaccount_list']
    columns = [
        ('Name', 'name'),
        ('Subaccount ID', 'subaccount_id'),        
    ]
    paginate_by = 50
    
    def get_queryset(self, *args, **kwargs):
        return super(SubaccountListView,self).get_queryset().order_by('subaccount_id','name')
    
class AssignmentListView(CurrentUserMixin, CCESearchView):
    model = Assignment
    page_title = 'Assignment List'
    search_form_class = AssignmentSimpleSearchForm
    advanced_search_form_class = AssignmentAdvancedSearchForm
    template_name = 'reloadable_list.html'
    sidebar_group = ['canvas', 'canvas_assignment_list']
    columns = [
        ('Course', 'course'),
        ('Name', 'name'),
        ('Assignment ID', 'assignment_id'),        
        ('Start Date', 'start_date'),
        ('Due Date', 'due_date'),
        ('End Date', 'end_date'),
        ('Has Override?', 'has_override'),
        ('Quiz?', 'is_quiz'),
    ]
    paginate_by = 50
    
    def get(self, request, *args, **kwargs):
        course_id = None
        if 'course_id' in self.kwargs:
            course_id = int(self.kwargs['course_id'])
        reload = request.GET.get('reload', False) == "True"
            
        if course_id is not None:
            existing_records = self.model.objects.filter(course__course_id = course_id).first()
            
            if existing_records is None or reload:
                api = CanvasAPI()
    
                course = Course.objects.filter(course_id = course_id).first()
                self.model.objects.filter(course = course).all().delete()
                json_data = api.get_assignments(course_id)
                json_list = list(json_data) #the data from canvas
                
                for assignment in json_list:   #get the stuff i need from the canvas data
                    assignment_id = assignment['id']
                    assignment_name = assignment['name']             
                    has_override = assignment['has_overrides']
                    is_quiz = assignment['is_quiz_assignment'] 
                    logging.warning("ASSIGNMENT")
                    logging.warning(str(assignment))
                    td = timedelta (hours = 6)#adjust to local time      
                    if assignment['unlock_at'] is not None:
                        unlockCanvas = datetime.strptime(assignment['unlock_at'], '%Y-%m-%dT%H:%M:%SZ')#save in datetime object
                        unlockCanvas = unlockCanvas - td#adjust time.  else it goes past midnight altering the date
                        start_date = datetime.strftime(unlockCanvas, '%Y-%m-%d')#remove time and save just the date as a string
                    else: 
                        start_date = None
                    if assignment['due_at'] is not None:
                        dueCanvas = datetime.strptime(assignment['due_at'], '%Y-%m-%dT%H:%M:%SZ')
                        dueCanvas = dueCanvas - td
                        due_date = datetime.strftime(dueCanvas, '%Y-%m-%d')#saving date as string and in m/d/y for use with datepicker
                    else:
                        due_date = None
                    if assignment['lock_at'] is not None:
                        lockCanvas = datetime.strptime(assignment['lock_at'], '%Y-%m-%dT%H:%M:%SZ')                
                        lockCanvas = lockCanvas - td 
                        end_date = datetime.strftime(lockCanvas, '%Y-%m-%d')
                    else:
                        end_date = None
                      
                    self.model.user_objects.create(assignment_id = assignment_id, name = assignment_name, start_date = start_date, due_date = due_date, end_date = end_date, has_override = has_override, is_quiz = is_quiz, course = course)
        
        return super(AssignmentListView, self).get(request, *args, **kwargs)
        
    
    def get_queryset(self, *args, **kwargs):
        queryset = super(AssignmentListView,self).get_queryset()
        
        course_id = None
        if 'course_id' in self.kwargs:
            course_id = self.kwargs['course_id']
        
        if course_id is not None:
            queryset = queryset.filter(course__course_id = int(course_id)).all().order_by('name')
        else:
            queryset = queryset.order_by('course__name', 'name')
        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super(AssignmentListView, self).get_context_data(*args, **kwargs) 
        course_id = None
        if 'course_id' in self.kwargs:
            course_id = int(self.kwargs['course_id'])
        
        if course_id is not None:
            context['course_id'] = course_id
            load_date = self.model.objects.filter(course__course_id = course_id).order_by('created_at').first()
            
            if load_date is not None:
                context['load_date'] = load_date.created_at
        
        return context

class UserCourseListView(CurrentUserMixin, CCESearchView):
    model = UserCourse
    page_title = 'User Course List'
    search_form_class = UserCourseSimpleSearchForm
    advanced_search_form_class = UserCourseAdvancedSearchForm
    template_name = 'reloadable_list.html'
    sidebar_group = ['canvas', 'canvas_usercourse_list']
    columns = [
        ('User', 'user'),        
        ('Course', 'course'),
    ]
    paginate_by = 50
    
    def get(self, request, *args, **kwargs):
        course_id = None
        if 'course_id' in self.kwargs:
            course_id = int(self.kwargs['course_id'])
        reload = request.GET.get('reload', False) == "True"
            
        if course_id is not None:
            existing_records = self.model.objects.filter(course__course_id = course_id).first()
            
            if existing_records is None or reload:
                api = CanvasAPI()
                course = Course.objects.filter(course_id = course_id).first()
                self.model.objects.filter(course = course).all().delete()
                
                user_list = api.get_users(course_id)
                for user in user_list:
                    localuser = User.objects.filter(canvas_id = int(user['id'])).first()
                    if localuser is not None:
                        self.model.user_objects.create(user = localuser, course = course)
        
        return super(UserCourseListView, self).get(request, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        queryset = super(UserCourseListView,self).get_queryset()
        
        course_id = None
        if 'course_id' in self.kwargs:
            course_id = self.kwargs['course_id']
        
        if course_id is not None:
            queryset = queryset.filter(course__course_id = int(course_id)).all().order_by('user__sortable_name')
            
        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserCourseListView, self).get_context_data(*args, **kwargs) 
        course_id = None
        if 'course_id' in self.kwargs:
            course_id = int(self.kwargs['course_id'])
        
        if course_id is not None:
            context['course_id'] = course_id
            load_date = self.model.objects.filter(course__course_id = course_id).order_by('created_at').first()
            
            if load_date is not None:
                context['load_date'] = load_date.created_at
        
        return context


####################################################
# Teacher Weekly Report Functions
####################################################

class TeacherWeeklyReportListView(CurrentUserMixin, CCEListView):
    model = TeacherWeeklyReport
    page_title = 'Teacher Weekly Report List'
    search_form_class = TeacherWeeklyReportSimpleSearchForm
    sidebar_group = ['canvas', 'twr_list']
    columns = [
        ('Year', 'year'),
        ('Week', 'week_number'),
        ('Start Date', 'start_date'),
        ('End Date', 'end_date'),
    ]
    
    def get_queryset(self):
        results = self.model.objects.all().distinct('year', 'week_number')
        return results
    
    def render_buttons(self, user, obj, *args, **kwargs):
        buttons = super(TeacherWeeklyReportListView, self).render_buttons(user, obj,
                                                            *args, **kwargs)
        
        buttons.append(
            self.render_button(btn_class='btn-warning btn-inline',
                               button_text='Download CSV',
                               icon_classes='glyphicon glyphicon-save',
                               url= "/c/twr/" + str(obj.year) + "/" + str(obj.week_number) + "/",
                               label="Download CSV",
                               condensed=False,)
        )
        
        return buttons
    
def teacherWeeklyReportCSVDownload(request, **kwargs):
    if 'year' in kwargs :
        try:
            year = int(kwargs['year'])
        except:
            year = None
    else:
        year = None    

    if 'week' in kwargs:
        try:
            week = int(kwargs['week'])
        except:
            week = None
    else:
        week = None 
    
    if week is None or year is None:
        return redirect('')
    
    twr = TeacherWeeklyReport.objects.filter(year = year, week_number = week)
    
    if hasattr(settings, 'CANVAS_COURSE_BASE_URL'):
        canvas_base_url = settings.CANVAS_COURSE_BASE_URL
    else:
        canvas_base_url = "https://canvas.ou.edu/courses/"
    

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=FacultyWeeklyReport_' + str(year) + '_' + str(week) + '.csv'
    writer = csv.writer(response)
    
    #Report Info
    first_record = twr.first()
    writer.writerow(["Year", "Week", "Start Date", "End Date"])
    writer.writerow([first_record.year, first_record.week_number, first_record.start_date, first_record.end_date])
    writer.writerow([])
    writer.writerow([])
    writer.writerow(["Course Link", "Course", "Teacher", "Last Login", "Announcement Posted", "Announcement Post Date"])
    writer.writerow(['', '', "Discussion", "Discussion ID", "Discussion Name", "Due Date", "Unique Entry Count", "Reply Count", "Reply %", "Teacher Unique Entry Count", "Submission Count", "Comment Count"])
    writer.writerow(['', '', "Assignment", "Assignment ID", "Assignment Name", "Due Date", "Submission Count", "Comment Count"])
    writer.writerow([])
    
    for twr_record in twr:
        course_url = canvas_base_url + str(twr_record.usercourse.course.course_id)
        writer.writerow([course_url, twr_record.usercourse.course.name, twr_record.usercourse.user.name, twr_record.last_login, twr_record.announcement_posted, twr_record.announcement_post_date])
        discussions = TeacherWeeklyReportDiscussions.objects.filter(teacherweeklyreport = twr_record)
        for disc in discussions:
            if disc.unique_entry_count == 0:
                reply_percent = 0
            else:
                reply_percent = ((float(disc.reply_count) / float(disc.unique_entry_count)) * 100)
            writer.writerow(['', '', "Discussion", disc.discussion_id, disc.discussion_name, disc.due_date, disc.unique_entry_count, disc.reply_count, reply_percent, disc.teacher_unique_entry_count, disc.submission_count, disc.submission_comment_count])
        assignments = TeacherWeeklyReportAssignments.objects.filter(teacherweeklyreport = twr_record)
        for assn in assignments:
            writer.writerow(['', '', "Assignment", assn.assignment_id, assn.assignment_name, assn.due_date, assn.submission_count, assn.comment_count])
    
    return response
    

