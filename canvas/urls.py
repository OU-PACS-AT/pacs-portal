# Django imports
from django.conf.urls import url, include

# Nucleus imports
from nucleus.decorators import is_staff, is_faculty, is_faculty_or_staff, is_student, is_admin

# View imports
from canvas.views import CourseListView as CanvasCourseListView, StudentListView as CanvasStudentListView

urlpatterns = [

    url(r'^courses/$', is_faculty_or_staff(CanvasCourseListView.as_view()),
        name='canvas_course_list'),

    url(r'^students/$', is_admin(CanvasStudentListView.as_view()),
        name='canvas_student_list'),

    ]

