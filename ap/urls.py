from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from ap.views import NewCourseRequests, ReviseCourseRequests, TextbookChangeRequests, RedevelopCourseRequests, AcceptanceDeclarations

urlpatterns = [
	url(r'^new_course_requests', login_required(NewCourseRequests.as_view()), name="new_course_requests"),
	url(r'^revise_course_requests', login_required(ReviseCourseRequests.as_view()), name="revise_course_requests"),
	url(r'^textbook_change_requests', login_required(TextbookChangeRequests.as_view()), name="textbook_change_requests"),
	url(r'^acceptance_declarations', login_required(AcceptanceDeclarations.as_view()), name="acceptance_declarations"),
	url(r'^redevelop_course_requests', login_required(RedevelopCourseRequests.as_view()), name="redevelop_course_requests"),

    # DEFAULT    
    #url(r'', DashboardView.as_view(), name="dashboard"),
]