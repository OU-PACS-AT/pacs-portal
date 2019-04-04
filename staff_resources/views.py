from django.shortcuts import render
# Create your views here.
from django.contrib import messages
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings

from canvasapi import Canvas
from django.views.generic import TemplateView
import requests, os, logging

# Toolkit imports
from toolkit.views import  CCETemplateView, CCECreateView, CCECreateWithInlinesView, CCEDeleteView, CCEDetailView, \
    CCEFormView, CCEListView, CCEModelFormSetView, CCEObjectRedirectView, CCERedirectView, \
    CCESearchView, CCETemplateView, CCEUpdateView,  CCEUpdateWithInlinesView, \
    ReportDownloadDetailView, ReportDownloadSearchView

# User Credentials retrieval/mixins
from nucleus.auth import UserCredentials
from nucleus.mixins import CurrentUserMixin
from forms import AnnouncementSimpleSearch, AnnouncementForm
from models import Announcement


class AnnouncementSearchView(CCESearchView):
    def __init__(self, *args, **kwargs):
        super(AnnouncementSearchView, self).__init__(*args, **kwargs)
        from nucleus.auth import UserCredentials
        creds = UserCredentials()
        self.model.objects.filter(created_by = creds.get_OUNetID()).delete()

class DashboardView(CurrentUserMixin, CCESearchView):
    sidebar_group = ['dashboard', ]
    template_name = 'dashboard.html'
    page_title = "Announcements"
    search_form_class = AnnouncementSimpleSearch
   
    success_message = "success"
    model = Announcement
    show_context_menu = True
    paginate_by = 10
    
    columns = [
        ('Title', 'name'),
        ('Body', 'body'),
        ('Author', 'author'),
        ('Date', 'last_updated_at'),
        ('School', 'school'), 
        ('Actions', 'short_school') ,       
    ]
    
    
    def get(self, request, *args, **kwargs):
        creds = UserCredentials()
        
        return super(DashboardView, self).get(request, *args, **kwargs)
        
    def get_queryset(self):
        return super(DashboardView, self).get_queryset()\
            .all().order_by('-last_updated_at' , 'name')
            
            
class AnounceCreateView(CurrentUserMixin, CCECreateView):
    model = Announcement
    form_class = AnnouncementForm
    page_title = "Add Announcement!"
    sidebar_group = ['dashboard', ]
    success_message = "Announcement Created Successfully"
    creds = UserCredentials()
    
    def get_success_url(self):
        return reverse('dashboard')
    
class AnounceUpdateView(CurrentUserMixin, CCEUpdateView):
    model = Announcement
    form_class = AnnouncementForm
    page_title = 'Edit Announcement'
    sidebar_group = ['dashboard', ]    
    success_message = "Announcement Edited Successfully"
    
    def get_success_url(self):
        return reverse('dashboard')


class AnounceDeleteView(CurrentUserMixin, CCEDeleteView):
    model = Announcement    
    page_title = 'Delete Announcement'    
    sidebar_group = ['dashboard', ]
    success_message = "Announcement Deleted Successfully"

    def get_success_url(self):
        return reverse('dashboard')
    
class PACSCourseRotation(CurrentUserMixin,CCETemplateView):
    sidebar_group = ['staff_resources', 'course_rotation']
    template_name = 'course_rotation.html'
    page_title = 'PACS Course Rotation'    
    
class CourseWorkloadEstimator(CurrentUserMixin,CCETemplateView):
    sidebar_group = ['staff_resources', 'workload-estimator']
    template_name = 'workload-estimator.html'
    page_title = 'Course Workload Estimator'     
    
class LearningOutcomeGenerator(CurrentUserMixin,CCETemplateView):
    sidebar_group = ['staff_resources', 'outcome-generator']
    template_name = 'outcome-generator.html'
    page_title = 'Learning Outcome Generator'     
    
class CropTool(CurrentUserMixin,CCETemplateView):
    sidebar_group = ['staff_resources', 'crop_tool']
    template_name = 'crop_tool.html'
    page_title = 'Crop Tool'			
        
class ButtonMaker(CurrentUserMixin,CCETemplateView):
    sidebar_group = ['staff_resources', 'button_maker']
    template_name = 'button_maker.html'
    page_title = 'Button Maker'		
	
class BannerMaker(CurrentUserMixin,CCETemplateView):
    sidebar_group = ['staff_resources', 'banner_maker']
    template_name = 'banner_maker.html'
    page_title = 'Banner Maker'			
       
class ObjectiveBuilder(CurrentUserMixin,CCETemplateView):
    sidebar_group = ['staff_resources', 'objective_builder']
    template_name = 'objective_builder.html'
    page_title = 'Objective Builder'        
       
class NewCourseTrello(CurrentUserMixin,CCETemplateView):
    sidebar_group = ['staff_resources', 'new-course-trello']
    template_name = 'new_course_template.html'
    page_title = 'Trello Boards'    
      
       