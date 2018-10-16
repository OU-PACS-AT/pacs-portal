"""cls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views


#from tasks.views import TaskListView


urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + [
                    url(r'^admin', include(admin.site.urls)),
                  
                    # Authentication URLs
                    url(r'^accounts/', include([
                        url(r'login/', 
                            auth_views.login,
                            {'template_name': 'registration/login.html',
                             'extra_context': {'sidebar_group': ['profiles','login']}
                             },
                            name='login', ),
                        url(r'logout/', 
                            auth_views.logout,
                            {'template_name': 'registration/logout.html',
                             'extra_context': {'sidebar_group': ['profiles','logout']}
                             },
                            name='logout', ),
                        url(r'password_change/', include([
                            url(r'done/', 
                                auth_views.password_change_done,
                                {'template_name': 'registration/password_change_complete.html'},
                                name='password_change_done', ),
                            url(r'',
                                auth_views.password_change,
                                {'template_name': 'registration/password_change.html',
                                 'extra_context': {'sidebar_group': ['profiles','password_change']}
                                 },
                                name='password_change', ),
                            ])),
                        url(r'password_reset/', include([
                            url(r'done/', 
                                auth_views.password_reset_done,
                                {'template_name': 'registration/password_reset_done.html',
                                 'extra_context': {'sidebar_group': ['profiles','password_reset_done']}
                                 },
                                name='password_reset_done', ),
                            url(r'',
                                auth_views.password_reset,
                                {'template_name': 'registration/password_reset_form.html',
                                 'email_template_name': 'registration/reset_password_email.html',
                                 'subject_template_name': 'registration/reset_password_subject.html',
                                 'extra_context': {'sidebar_group': ['profiles','password_reset']}
                                 },
                                name='password_reset', ),
                            ])),
                        url(r'', include('django.contrib.auth.urls')),
                    ])),

                    # User Profiles
                    url(r'^profiles/', include("profiles.urls")),
                  
                    # Apps 
                    url(r'', include("resources.urls")),
                    
              ]

