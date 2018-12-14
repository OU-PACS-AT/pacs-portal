from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from nucleus.decorators import is_staff, is_faculty, is_student

from staff_resources.views import DashboardView, CropTool, ButtonMaker, BannerMaker, ObjectiveBuilder

urlpatterns = [
	url(r'^crop_tool', is_staff(CropTool.as_view()), name="crop_tool"),
	url(r'^button_maker', is_staff(ButtonMaker.as_view()), name="button_maker"),
	url(r'^banner_maker', is_staff(BannerMaker.as_view()), name="banner_maker"),
	url(r'^objective_builder', is_staff(ObjectiveBuilder.as_view()), name="objective_builder"),

    # DEFAULT    
    url(r'', DashboardView.as_view(), name="dashboard"),
]