from toolkit.helpers.admin import auto_admin_register
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect

# Nucleus Imports
from nucleus.api import CanvasAPI
from nucleus.auth import UserCredentials 
from nucleus import settings

# Model Imports
from models import Submission, Assignment

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_id', 'name', 'course')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment')

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)

auto_admin_register(__package__)