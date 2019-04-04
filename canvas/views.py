from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

# Nucleus imports 
from nucleus.mixins import CurrentUserMixin
from nucleus.auth import UserCredentials
from nucleus.api import CanvasAPI

# Library imports
from datetime import datetime, timedelta, tzinfo, date, time
import logging
import requests

# Toolkit views
from toolkit.views import CCECreateView, CCECreateWithInlinesView, CCEDeleteView, CCEDetailView, \
    CCEFormView, CCEListView, CCEModelFormSetView, CCEObjectRedirectView, CCERedirectView, \
    CCESearchView, CCETemplateView, CCEUpdateView,  CCEUpdateWithInlinesView, \
    ReportDownloadDetailView, ReportDownloadSearchView

# Form imports
from forms import CourseSimpleSearchForm, CourseAdvancedSearchForm, StudentSimpleSearchForm, AssignmentSimpleSearchForm, StudentCourseSimpleSearchForm
from models import Course, Student, StudentCourse, Assignment, Term, SubAccount


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
    
class StudentListView(CurrentUserMixin, CCESearchView):
    model = Student
    page_title = 'Student List'
    search_form_class = StudentSimpleSearchForm
    sidebar_group = ['canvas', 'student_list']
    columns = [
        ('Name', 'name'),
        ('Login ID', 'login_id'),        
        ('Canvas ID', 'canvas_id'),
        ('SIS ID', 'sis_user_id'),
    ]
    paginate_by = 50
    
class AssignmentListView(CurrentUserMixin, CCESearchView):
    model = Assignment
    page_title = 'Assignment List'
    search_form_class = AssignmentSimpleSearchForm
    sidebar_group = ['canvas', 'assignment_list']
    columns = [
        ('Name', 'name'),
        ('Assignment ID', 'assignment_id'),        
        ('Course', 'course'),
        ('Quiz?', 'is_quiz_assignment'),
    ]
    paginate_by = 50
    
class StudentCourseListView(CurrentUserMixin, CCESearchView):
    model = StudentCourse
    page_title = 'Student Course List'
    search_form_class = StudentCourseSimpleSearchForm
    sidebar_group = ['canvas', 'studentcourse_list']
    columns = [
        ('Student', 'student'),        
        ('Course', 'course'),
    ]
    paginate_by = 50
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        queryset = super(StudentCourseListView,self).get_queryset()
        if course_id is not None:
            queryset = queryset.filter(course__course_id = int(course_id)).all().order_by('student__name')
        return queryset
    