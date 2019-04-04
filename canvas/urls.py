# Django imports
from django.conf.urls import url, include

# Nucleus imports
from nucleus.decorators import is_staff, is_faculty, is_faculty_or_staff, is_student, is_admin

# View imports
from canvas.views import CourseListView as CanvasCourseListView, StudentListView as CanvasStudentListView, AssignmentListView as CanvasAssignmentListView, StudentCourseListView as CanvasStudentCourseListView

urlpatterns = [

    url(r'^courses/$', is_faculty_or_staff(CanvasCourseListView.as_view()),
        name='canvas_course_list'),

    url(r'^students/$', is_admin(CanvasStudentListView.as_view()),
        name='canvas_student_list'),

    url(r'^assignments/$', is_admin(CanvasAssignmentListView.as_view()),
        name='canvas_assignment_list'),

    url(r'^(?P<course_id>\d+)/students/$', is_admin(CanvasStudentCourseListView.as_view()),
        name='canvas_studentcourse_list'),

       
    ]

