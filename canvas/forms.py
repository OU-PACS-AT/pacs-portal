# Django Imports
from django import forms
from django.forms import BaseFormSet
from django.utils.translation import ugettext as _

from datetime import datetime, timedelta, tzinfo, date, time

# Toolkit base forms
from toolkit.forms import CCESimpleSearchForm, CCEModelSearchForm, CCEModelForm

# Models
from models import Course, User, Term, Subaccount, UserCourse
from models import TeacherWeeklyReport, TeacherWeeklyReportAssignments, TeacherWeeklyReportDiscussions
from faculty_tools.models import Assignment

import logging

class TeacherWeeklyReportSimpleSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search Reports'

    class Meta(CCESimpleSearchForm.Meta):
        model = TeacherWeeklyReport
        field_lookups = {'search': ('usercourse__course__name__icontains',
                                    'usercourse__user__name__icontains')}

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

class UserSimpleSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search Users'

    class Meta(CCESimpleSearchForm.Meta):
        model = User
        field_lookups = {'search': ('canvas_id__icontains',
                                    'name__icontains',
                                    'sortable_name__icontains',
                                    'sis_user_id__icontains',
                                    'login_id__icontains')}


class TermSimpleSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search Terms'

    class Meta(CCESimpleSearchForm.Meta):
        model = Term
        field_lookups = {'search': ('term_id__icontains',
                                    'name__icontains')}

class SubaccountSimpleSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search Subaccounts'

    class Meta(CCESimpleSearchForm.Meta):
        model = Subaccount
        field_lookups = {'search': ('subaccount_id__icontains',
                                    'name__icontains')}

      
class AssignmentSimpleSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search Assignments'

    class Meta(CCESimpleSearchForm.Meta):
        model = Assignment
        field_lookups = {'search': ('assignment_id__icontains',
                                    'name__icontains',
                                    'course__course_code__icontains',
                                    'course__course_id__icontains',
                                    'course__name__icontains')}
        
class AssignmentAdvancedSearchForm(CCEModelSearchForm):

    class Meta:
        model = Assignment
        field_lookups = {
            'name': ('name__icontains', 'assignment_id__icontains'),
            'course': ('course__course_code__icontains', 'course__name__icontains', 'course__course_id__icontains'),
        }

        fields = (
            'name',
            'course',
        )

        labels = {
            'name': 'Assignment',
            'course': 'Course',
        }
        
class UserCourseSimpleSearchForm(CCESimpleSearchForm):
    search_placeholder = 'Search User/Course Mapping'

    class Meta(CCESimpleSearchForm.Meta):
        model = UserCourse
        field_lookups = {'search': ('user__name__icontains',
                                    'course__name__icontains',
                                    'course__course_code__icontains',
                                    'user__sortable_name__icontains',
                                    'user__sis_user_id__icontains',
                                    'user__login_id__icontains')}  

class UserCourseAdvancedSearchForm(CCEModelSearchForm):

    class Meta:
        model = UserCourse
        field_lookups = {
            'user': ('user__name__icontains', 'user__sortable_name__icontains'),
            'course': ('course__course_code__icontains', 'course__name__icontains', 'course__course_id__icontains'),
        }

        fields = (
            'user',
            'course',
        )

        labels = {
            'user': 'User',
            'course': 'Course',
        }

