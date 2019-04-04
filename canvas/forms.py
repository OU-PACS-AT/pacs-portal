# Django Imports
from django import forms
from django.forms import BaseFormSet
from django.utils.translation import ugettext as _

from datetime import datetime, timedelta, tzinfo, date, time

# Toolkit base forms
from toolkit.forms import CCESimpleSearchForm, CCEModelSearchForm, CCEModelForm

# Models
from models import Course, Student, Assignment, StudentCourse

import logging

class CourseSimpleSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search Courses'

    class Meta(CCESimpleSearchForm.Meta):
        model = Course
        field_lookups = {'search': ('id__icontains',
                                    'name__icontains',
                                    'course_code__icontains')}

class CourseAdvancedSearchForm(CCEModelSearchForm):

    class Meta:
        model = Course
        field_lookups = {
            'name': ('name__icontains', 'course_code__icontains'),
            'course_id': ('course_id__icontains'),
            'subaccount': 'subaccount',
            'term': 'term',
        }

        fields = (
            'name',
            'course_id',
            'subaccount',
            'term',
        )

        labels = {
            'name': 'Course Name/Code',
            'course_id': 'Course ID',
            'subaccount': 'Subaccount',
            'term': 'Term',
        }

class StudentSimpleSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search Students'

    class Meta(CCESimpleSearchForm.Meta):
        model = Student
        field_lookups = {'search': ('canvas_id__icontains',
                                    'name__icontains',
                                    'sortable_name__icontains',
                                    'sis_user_id__icontains',
                                    'login_id__icontains')}
        
        
class AssignmentSimpleSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search Assignments'

    class Meta(CCESimpleSearchForm.Meta):
        model = Assignment
        field_lookups = {'search': ('assignment_id__icontains',
                                    'name__icontains',
                                    'course__name__icontains')}
        
class StudentCourseSimpleSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search Students'

    class Meta(CCESimpleSearchForm.Meta):
        model = StudentCourse
        field_lookups = {'search': ('student__name__icontains',
                                    'student__sortable_name__icontains',
                                    'student__sis_user_id__icontains',
                                    'student__login_id__icontains')}        
