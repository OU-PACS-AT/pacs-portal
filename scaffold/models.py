from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

from toolkit.models import CCEAuditModel


class PACSModel(models.Model):
    """
    Abstract model with fields for the user and timestamp of a row's creation
    and last update.
    .. note:: - 
    """
    from nucleus.auth import UserCredentials
    
    creds = UserCredentials()
    
    last_updated_by = models.CharField(max_length=8, default=creds.get_OUNetID())
    last_updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=8, default=creds.get_OUNetID())
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
    
    @property
    def tz_last_updated_at(self):
        from django.utils.timezone import localtime
        return localtime(self.last_updated_at)
    
    @property
    def tz_created_at(self):
        from django.utils.timezone import localtime
        return localtime(self.created_at)

    def can_update(self, user_obj):
        return True

    def can_delete(self, user_obj):
        return True

    def can_create(self, user_obj):
        return True

    def can_view_list(self, user_obj):
        return True

    def can_view(self, user_obj):
        return True


class Course(PACSModel):
    course_id = models.IntegerField()
    name = models.CharField(max_length = 100)
    
    def __unicode__(self):
        return u'{0}'.format(self.class_name)

    def get(self):
        return self.class_name

    def get_absolute_url(self):
        return reverse('course_list') + '?course=%s' % self.pk

    
class Assignment(PACSModel):
    course_id = models.IntegerField()
    assignment_number = models.IntegerField(unique = False)
    assignment_name = models.CharField(max_length = 100)
    start_date = models.CharField(max_length = 10)
    due_date = models.CharField(max_length = 10)
    end_date = models.CharField(max_length = 10)
    
    #def _str_(self):
    #    return self.assignment_number, self.assignment_name, self.start_date, self.due_date, self.end_date

    def __unicode__(self):
        return u'{0}'.format(self.assignment_name)
        
    def get(self):
        return self.assignment_number
    

    



