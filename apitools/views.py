from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib import messages
from django.template import RequestContext
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings

from itertools import izip
from datetime import datetime, timedelta, tzinfo, date, time
from urllib2 import HTTPError
from canvasapi import Canvas

import logging
import json
import requests
import pytz
import dateutil 

#from apitools.models import CanvasAssignment
#from apitools.models import CanvasClass
#from apitools.models import CanvasStudent
#from apitools.forms import GetClassNumber
#from apitools.forms import TableForm
#from apitools.forms import TableFormSet
#from apitools.forms import ConfirmForm
#from apitools.forms import XTableForm
#from apitools.forms import XTableFormSet
#from apitools.forms import StudentForm
#from apitools.forms import XAssignmentForm
from apitools.api import GroupSetBuilder
from apitools.api import CanvasAPI


from toolkit.views import  CCETemplateView
# Create your views here.

class changeDates(CCETemplateView):
    sidebar_group = ['apitools', 'Change Dates']
    page_title = 'Change Dates' 
    template_name = 'find.html'           

 