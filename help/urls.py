# Django imports
from django.conf.urls import url, include

# Nucleus imports
from nucleus.decorators import is_admin, is_member

# View imports
from help.views import UserGuides

urlpatterns = [

    url(r'^user_guides', UserGuides.as_view(), name="user_guides"),

    
    ]

