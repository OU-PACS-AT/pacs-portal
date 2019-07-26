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
from toolkit.views import  CCETemplateView

# User Credentials retrieval/mixins
from nucleus.auth import UserCredentials
from nucleus.mixins import CurrentUserMixin

class UserGuides(CurrentUserMixin,CCETemplateView):
    sidebar_group = ['help', 'user_guides']
    template_name = 'user_guides.html'
    page_title = 'User Guides'  