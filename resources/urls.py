from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from resources.views import DashboardView, CropTool, ButtonMaker, BannerMaker, ObjectiveBuilder

urlpatterns = [
	url(r'^crop_tool', login_required(CropTool.as_view()), name="crop_tool"),
	url(r'^button_maker', login_required(ButtonMaker.as_view()), name="button_maker"),
	url(r'^banner_maker', login_required(BannerMaker.as_view()), name="banner_maker"),
	#url(r'^objective_builder', login_required(ObjectiveBuilder.as_view()), name="objective_builder"),

    # DEFAULT    
    url(r'', DashboardView.as_view(), name="dashboard"),
]