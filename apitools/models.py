from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from pickle import FALSE

from scaffold.models import PACSModel

# Create your models here.

class CanvasClass(PACSModel):
    class_number = models.IntegerField(unique = False)
    class_name = models.CharField(max_length = 100)
    
    def get(self):
        return self.class_name
    
    def __unicode__(self):
        return u'{0}'.format(self.class_name)


class CanvasAssignment(PACSModel):
    assignment_number = models.IntegerField(unique = False)
    assignment_name = models.CharField(max_length = 100)
    start_date = models.CharField(max_length = 10)
    due_date = models.CharField(max_length = 10)
    end_date = models.CharField(max_length = 10)
    class_number = models.IntegerField()
    
	
    def _str_(self):
        return self.assignment_number, self.assignment_name, self.start_date, self.due_date, self.end_date
    
    def __unicode__(self):
        return u'{0}'.format(self.assignment_name)
    
    def get(self):
        return self.assignment_number
    
class CanvasStudent(PACSModel):
    student_id = models.IntegerField(unique = False)
    student_name = models.CharField(max_length = 100)
    checked = models.BooleanField(default = False)
    class_number = models.IntegerField()
    
    def __unicode__(self):
        return u'{0}'.format(self.student_name)
    
    def _str_(self):
        return u'{0}'.format(self.student_name)

