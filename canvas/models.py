from __future__ import unicode_literals
from django.db import models

# Nucleus imports
from nucleus.models import PACSModel

class Term(PACSModel):
    term_id = models.IntegerField(unique=True)
    name = models.CharField(max_length = 100)

    class Meta:
        ordering = ('term_id',)
        
    def _str_(self):
        return self.term_id, self.name 
    
    def __unicode__(self):
        return u'{0}'.format(self.name)

    def get(self):
        return self.name

class SubAccount(PACSModel):
    parent = models.ForeignKey('self', null=True, related_name='subaccount', on_delete=models.CASCADE,)
    subaccount_id = models.IntegerField(unique = True)
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = "Subaccounts"
        ordering = ('name',)

    def _str_(self):
        return self.subaccount_id, self.parent, self.name 
    
    def __unicode__(self):
        return u'{0}'.format(self.name)

    def get(self):
        return self.name

class Course(PACSModel):
    course_id = models.IntegerField(null = True, unique=True)
    name = models.CharField(max_length = 100)
    course_code = models.CharField(max_length = 100)
    term = models.ForeignKey(Term, null=True, on_delete=models.CASCADE,)
    subaccount = models.ForeignKey(SubAccount, null = True, on_delete=models.CASCADE,)
    
    class Meta:
        ordering = ('course_code','name',)
    
    def _str_(self):
        return self.course_id, self.name, self.course_code, self.subaccount_id

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def get(self):
        return self.name
    
class Student(PACSModel):
    canvas_id = models.IntegerField(unique = True)
    name = models.CharField(max_length = 100, null = True)
    sortable_name = models.CharField(max_length = 100, null = True)
    short_name = models.CharField(max_length = 100, null = True)
    sis_user_id = models.CharField(max_length = 100, null = True)
    login_id = models.CharField(max_length = 100)

    class Meta:
        ordering = ('name',)

    def _str_(self):
        return self.login_id, self.name, self.canvas_id, self.sis_user_id  
    
    def __unicode__(self):
        return u'{0}'.format(self.name)

    def get(self):
        return self.login_id
    
#class StudentCourse(PACSModel):
#    student = models.ForeignKey(Student)
#    course = models.ForeignKey(Course)

#    class Meta:
#        verbose_name_plural = "StudentCourses"
#        ordering = ('student','course')

#    def _str_(self):
#        return self.student, self.course  
    
#    def __unicode__(self):
#        return u'{0}'.format(self.student)

#    def get(self):
#        return self.student
    
#class Assignment(PACSModel):
#    assignment_id = models.IntegerField(unique = True)
#    name = models.CharField(max_length = 500, null = True)
#    is_quiz_assignment = models.BooleanField()
#    course = models.ForeignKey(Course)

#    class Meta:
#        ordering = ('course', 'name')

#    def _str_(self):
#        return self.name  
    
#    def __unicode__(self):
#        return u'{0}'.format(self.name)

#    def get(self):
#        return self.name