from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from resources.views import DashboardView, CropTool, ButtonMaker, BannerMaker

# Testing
from resources.views import CourseChangeRequest, CourseData

# Deprecating
from resources.views import GradeCalculator, CourseSchedule

urlpatterns = [
	url(r'^crop_tool', login_required(CropTool.as_view()), name="crop_tool"),
	url(r'^button_maker', login_required(ButtonMaker.as_view()), name="button_maker"),
	url(r'^banner_maker', login_required(BannerMaker.as_view()), name="banner_maker"),

    # Testing
    url(r'^course_data', CourseData.as_view(), name="course_data"),
    url(r'^course_change_request', login_required(CourseChangeRequest.as_view()), name="course_change_request"),

    # Deprecating
    url(r'^grade_calculator', login_required(GradeCalculator.as_view()), name="grade_calculator"),
    url(r'^course_schedule/(?P<units>\d+)/$', login_required(CourseSchedule.as_view()), name="course_schedule"),

    # DEFAULT    
    url(r'', DashboardView.as_view(), name="dashboard"),
]