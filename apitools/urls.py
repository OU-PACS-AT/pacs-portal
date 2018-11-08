
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required



from apitools.views import changeDates

urlpatterns = [

	#url(r'', changeDates.as_view(), name='changeDates'),
	url(r'^changeDates', login_required(changeDates.as_view()), name="changeDates"),
	
]