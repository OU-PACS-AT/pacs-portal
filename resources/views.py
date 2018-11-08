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
import requests, os, logging


# Toolkit imports
from toolkit.views import  CCETemplateView, CCECreateView

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
       
class ObjectiveBuilder(CCETemplateView):
    sidebar_group = ['resources', 'objective_builder']
    template_name = 'objective_builder.html'
    page_title = 'Objective Builder'        
       
 
       