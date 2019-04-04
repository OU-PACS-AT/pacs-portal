# Django imports
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

# Nucleus imports
from nucleus.models import PACSModel
from canvas.models import Student as CanvasStudent, Assignment as CanvasAssignment

class Course(PACSModel):
    course_id = models.IntegerField()
    name = models.CharField(max_length = 100)
    

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def get(self):
        return self.class_name

class Assignment(PACSModel):
    course_id = models.IntegerField(unique = False)
    assignment_id = models.IntegerField(unique = False)
    name = models.CharField(max_length = 100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    has_override = models.BooleanField(default = False)
    is_quiz = models.BooleanField(default = False)
    
    def _str_(self):
        return self.assignment_id, self.name, self.start_date, self.due_date, self.end_date, self.has_override, self.is_quiz

    def __unicode__(self):
        return u'{0}'.format(self.name)
        
    def get(self):
        return self.assignment_id
    
class Student(PACSModel):
    course_id = models.IntegerField(unique = False)
    student_id = models.IntegerField(unique = False)
    name = models.CharField(max_length = 100, null=True, blank=True)
    
    def _str_(self):
        return self.student_id, name

    def __unicode__(self):
        return u'{0}'.format(self.name)
        
    def get(self):
        return self.name
    
class Submissions(PACSModel):
    student = models.ForeignKey(CanvasStudent, null = True)
    assignment = models.ForeignKey(CanvasAssignment, null = True)
    submitted = models.BooleanField(default = False)
    late = models.BooleanField(default = False)
    
    def _str_(self):
        return self.student, self.assignment, self.submitted, self.late
    
    def __unicode__(self):
        return u'{0}'.format(self.student, self.assignment)
        
    def get(self):
        return self.student, self.assignment, self.submitted, self.late
    
    