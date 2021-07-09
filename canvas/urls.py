# Django imports
from django.conf.urls import url, include

# Nucleus imports
from nucleus.decorators import is_admin, is_member

# View imports
from canvas.views import AdminCourseListView, CourseListView, UserListView, SubaccountListView, TermListView
from canvas.views import AssignmentListView, UserCourseListView
from canvas.views import TeacherWeeklyReportListView, teacherWeeklyReportCSVDownload

urlpatterns = [

    url(r'^course/$', is_member(CourseListView.as_view(), ["PACSATAdvising"]),
        name='canvas_course_list'),

    url(r'^admincourse/$', is_admin(AdminCourseListView.as_view()),
        name='canvas_admincourse_list'),

    # 2021-07-09 Will Poillion
    # Added for TeacherWeeklyReport list and download
    # Need permissions on these!!
    url(r'^twr/', include([
        url(r'^(?P<year>\d+)/(?P<week>\d+)/$', teacherWeeklyReportCSVDownload,
            name='twr_download'),
        url(r'^$', TeacherWeeklyReportListView.as_view(),
            name='twr_list'),   
    ])),

    # 2021-06-09 Will Poillion
    # Added to represent generic user table as holds teachers as well as students
    url(r'^user/$', is_admin(UserListView.as_view()),
        name='canvas_user_list'),
    url(r'^usercourse/', include([
        url(r'^(?P<course_id>\d+)/$', is_admin(UserCourseListView.as_view()),
            name='canvas_usercourse_list_course_id'),
        url(r'$', is_admin(UserCourseListView.as_view()),
            name='canvas_usercourse_list'),   
    ])),

    url(r'^assignment/', include([
        url(r'^(?P<course_id>\d+)/$', is_admin(AssignmentListView.as_view()),
            name='canvas_assignment_list_course_id'),
        url(r'$', is_admin(AssignmentListView.as_view()),
            name='canvas_assignment_list'),   
    ])),
                                           

    url(r'^subaccount/$', is_admin(SubaccountListView.as_view()),
        name='canvas_subaccount_list'),

    url(r'^term/$', is_admin(TermListView.as_view()),
        name='canvas_term_list'),

    ]

