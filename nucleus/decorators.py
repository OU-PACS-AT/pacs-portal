from django.core.exceptions import PermissionDenied
from nucleus.auth import UserCredentials

def is_staff(function):
    
    def wrap(request, *args, **kwargs):
        creds = UserCredentials()
        if creds.is_staff():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
    
def is_faculty(function): 
    
    def wrap(request, *args, **kwargs):
        creds = UserCredentials()
        if creds.is_faculty():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def is_student(function):

    def wrap(request, *args, **kwargs):
        creds = UserCredentials()
        if creds.is_student():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def is_faculty_or_staff(function):

    def wrap(request, *args, **kwargs):
        creds = UserCredentials()
        if creds.is_faculty or creds.is_staff():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def is_admin(function):

    def wrap(request, *args, **kwargs):
        creds = UserCredentials()
        if creds.is_admin():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


