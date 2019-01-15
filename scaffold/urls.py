from django.conf.urls import url, include

from scaffold.views import CourseListView, EditDueDates

from nucleus.decorators import is_staff, is_faculty, is_student, is_admin

urlpatterns = [


    url(r'^(?P<course_id>\d+)/', include([
        url(r'^edit/$', is_admin(EditDueDates.as_view()),
            name='edit_due_dates'),
    #    url(r'^delete/$', is_admin(BoardDeleteView.as_view()),
    #        name='delete_board'),
    ])),
    #url(r'^create_board/', is_admin(BoardCreateView.as_view()),
    #    name='add_board', ),
    url(r'', is_admin(CourseListView.as_view()),
        name='course_list', ),
    #url(r'', login_required(DashboardView.as_view()),
    #    name='dashboard', ),
]
