# Django imports
from django.conf.urls import url, include

# Nucleus imports
from nucleus.decorators import is_staff, is_faculty, is_faculty_or_staff, is_student, is_admin

# View imports
from faculty_tools.views import CourseListView, EditDueDates, AssignmentListView, StudentListView, SubmissionListView 
from canvas.views import CourseListView as CanvasCourseListView

urlpatterns = [

    url(r'^course_list/', include([
        url(r'^(?P<course_id>\d+)/', include([
            url(r'^edit/$', is_faculty(EditDueDates.as_view()),
                name='edit_due_dates'),
        ])),
        url(r'^(?P<course_id>\d+)/', include([
            url(r'^extend/$', is_admin(AssignmentListView.as_view()), 
                name='assignment_list'),
            url(r'^(?P<assignment_id>\d+)/', include([
                url(r'^extend/$', is_admin(StudentListView.as_view()),
                    name='student_list'),
                url(r'^(?P<student_id>\d+)/', include([
                    url(r'^extend/$', is_admin(EditDueDates.as_view()),
                        name='extend_dates'),
                ])),
            ]))
        ])), 
        url(r'^(?P<course_id>\d+)/', include([
            url(r'^submissions/$', is_faculty(SubmissionListView.as_view()),
                name='view_submissions'),
        ])),
        url(r'',is_faculty(CourseListView.as_view()),
            name='course_list', ),
    ])),
               

    url(r'^canvas_course_list/', include([ 
        url(r'^(?P<course_id>\d+)/', include([
            url(r'^submissions/$', is_faculty(SubmissionListView.as_view()),
                name='view_submissions'),
        ])),
        url(r'', is_faculty(CanvasCourseListView.as_view()),
            name='canvas_course_list'),
    ])),

       
    ]

