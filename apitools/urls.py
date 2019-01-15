
from django.conf.urls import url, include

from apitools.views import changeDates
from apitools.views import extendDates

from apitools.views import CourseListView
from apitools.views import AssignmentListView
from apitools.views import StudentListView


from nucleus.decorators import is_staff, is_faculty, is_student, is_admin

urlpatterns = [


    #url(r'^(?P<student_id>\d+)/', include([
    #    url(r'^extend/$/assignment/$/student/$', is_admin(extendDates.as_view()),
    #        name='extendDates'),])),
    
    #url(r'^(?P<assignment_id>\d+)/', include([
    #    url(r'^extend/$/assignment/$', is_admin(StudentListView.as_view()),
    #        name='student_lists'),])),    
    
    url(r'^(?P<course_id>\d+)/', include([
        url(r'^edit/$', is_admin(changeDates.as_view()),
            name='changeDates'),])),
    
    url(r'^(?P<course_id>\d+)/', include([
        url(r'^extend/$', is_admin(changeDates.as_view()),
            name='assignment_lists'),])),
    
    url(r'^(?P<assignment_id>\d+)/', include([
        url(r'^assignment/$', is_admin(changeDates.as_view()),
            name='student_lists'),])),
    
    url(r'^(?P<student_id>\d+)/', include([
        url(r'^student/$', is_admin(changeDates.as_view()),
            name='extendDates'),])),
    

    
   # url(r'^(?P<course_id>\d+)/', include([
    #    url(r'^extend/$', is_admin(AssignmentListView.as_view()), 
    #        name='assignment_lists'), 
     #   url(r'^(?P<assignment_id>\d+)/$', include([
      #      url(r'^assignment/$', is_admin(StudentListView.as_view()), 
       #         name='student_lists'), 
        #    url(r'^(?P<student_id>\d+)/', include([
         #       url(r'^student/$', is_admin(extendDates.as_view()),
          #          name='extendDates'),
           # ])),    
        #])),
    #])),
        


    url(r'', is_admin(CourseListView.as_view()),
        name='course_lists', ),

    ]

