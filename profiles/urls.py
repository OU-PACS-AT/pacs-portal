from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from profiles.views import RegistrationView, SecondaryEmailChange


urlpatterns = [
    url(r'^register/', RegistrationView.as_view(), name="registration"),
    url(r'^secondary_email_change/', login_required(SecondaryEmailChange.as_view()), name="secondary_email_change"),
]