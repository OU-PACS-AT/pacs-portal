from django.shortcuts import render
# Create your views here.
from django.contrib import messages
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from canvasapi import Canvas
from django.views.generic import TemplateView
import requests


# Toolkit imports
from toolkit.views import  CCETemplateView, CCECreateView

from resources.forms import CourseChangeRequestForm
from resources.models import CourseChangeRequest

class DashboardView(CCETemplateView):
    sidebar_group = ['dashboard', ]
    template_name = 'dashboard.html'

    def get_page_title(self):
        return "Welcome Back"
        #return "Welcome Back %s" % self.request.user.get_full_name()
		
class CropTool(CCETemplateView):
    sidebar_group = ['resources', 'crop_tool']
    template_name = 'crop_tool.html'
    page_title = 'Crop Tool'			
		
class ButtonMaker(CCETemplateView):
    sidebar_group = ['resources', 'button_maker']
    template_name = 'button_maker.html'
    page_title = 'Button Maker'		
	
class BannerMaker(CCETemplateView):
    sidebar_group = ['resources', 'banner_maker']
    template_name = 'banner_maker.html'
    page_title = 'Banner Maker'			
       

       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
######################## Testing #############################
# Not currently in use
class CourseChangeRequest(CCECreateView):
    model = CourseChangeRequest
    form_class = CourseChangeRequestForm
    sidebar_group = ['resources', 'course_change_request']
    page_title = 'Create new Course Change Request'
    success_message = "Course Change Request Submitted!"    
        
class CourseData(TemplateView):
    sidebar_group = ['resources','course_data']
    template_name = 'course_data.html'
    page_title = 'Course Data'
    
    def get_context_data(self, **kwargs):
        #print "CANVAS_URL: " + settings.CANVAS_URL
        #print "CANVAS_TOKEN: " + settings.CANVAS_TOKEN
        context = super(CourseData, self).get_context_data(**kwargs)
        
        url = "https://canvas.ou.edu/api/v1/courses"
        headers = {"Authorization":"Bearer 8808~1HTPVyS2HJGvVKFyDCaPxGVzi1Kygy7TI0czE8E4F523EUWGcpKvOA7p9TJZnJIr"}
        
        r = requests.get(url, headers=headers)
        
        #canvas = Canvas(settings.CANVAS_URL, settings.CANVAS_TOKEN)
        
        context["courses"] = r.content
        
        #courses = canvas.get_courses()
        #print "Course[0]: " + courses[0]
        #course = canvas.get_course(79617)
        
        #course.update(name='AT Snow Day2')
        
        #course = courses[0]
        #course_id = courses[0].id
        #course = str(courses[0].name)
        #context["course_name"] = course_name
        #course = canvas.get_course(75298)
        return context

######################## Deprecating #############################
# In process of deprecation
class GradeCalculator(CCETemplateView):
    sidebar_group = ['resources', 'grade_calculator']
    template_name = 'grade_calculator.html'
    page_title = 'Grade Calculator'

class CourseSchedule(CCETemplateView):
    sidebar_group = ['resources']
    page_title = 'Course Schedule'
    
    def get_context_data(self, **kwargs):
        context = super(CourseSchedule, self).get_context_data(**kwargs)
        units = self.kwargs['units']
        context['combined_url'] = 'course_schedule' + units
        print "combined_url: " + context['combined_url']
        self.template_name = 'course_schedule' + units + '.html'
        self.sidebar_group.append(context['combined_url'])
        return context