from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from nucleus.decorators import is_staff, is_faculty, is_student

from staff_resources.views import DashboardView, CropTool, ButtonMaker, BannerMaker, ObjectiveBuilder, AnounceUpdateView, AnounceDeleteView, AnounceCreateView, PACSCourseRotation, CourseWorkloadEstimator, LearningOutcomeGenerator

urlpatterns = [
	url(r'^outcome-generator', is_staff(LearningOutcomeGenerator.as_view()), name="outcome-generator"),
	url(r'^workload-estimator', is_staff(CourseWorkloadEstimator.as_view()), name="workload-estimator"),
	url(r'^course_rotation', is_staff(PACSCourseRotation.as_view()), name="course_rotation"),
	url(r'^crop_tool', is_staff(CropTool.as_view()), name="crop_tool"),
	url(r'^button_maker', is_staff(ButtonMaker.as_view()), name="button_maker"),
	url(r'^banner_maker', is_staff(BannerMaker.as_view()), name="banner_maker"),
	url(r'^objective_builder', is_staff(ObjectiveBuilder.as_view()), name="objective_builder"),
	
	url(r'^(?P<pk>\d+)/', include([
        url(r'^edit/$', AnounceUpdateView.as_view(),
            name='edit_announcement'),
        url(r'^delete/$', AnounceDeleteView.as_view(),
            name='delete_announcement'),		   
    ])),
    url(r'^create/', AnounceCreateView.as_view(),
        name='add_announcement', ),
   
    # DEFAULT    
    url(r'', DashboardView.as_view(), name="dashboard"),
    
]