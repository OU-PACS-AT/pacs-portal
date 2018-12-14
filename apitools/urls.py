
from django.conf.urls import url, include

from apitools.views import changeDates
from apitools.views import extendDates

from apitools.views import CourseListView

from nucleus.decorators import is_staff, is_faculty, is_student, is_admin

urlpatterns = [


    url(r'^(?P<course_id>\d+)/', include([
        url(r'^edit/$', is_admin(changeDates.as_view()),
            name='changeDates'),])),
	
	url(r'^(?P<course_id>\d+)/', include([
        url(r'^edit/$', is_admin(extendDates.as_view()),
            name='extendDates'),])),
	

    url(r'', is_admin(CourseListView.as_view()),
        name='course_lists', ),

	]

