from __future__ import unicode_literals
from django.db import models

# Nucleus imports
from nucleus.models import PACSModel, ReportModel

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

class Subaccount(PACSModel):
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
    subaccount = models.ForeignKey(Subaccount, null = True, on_delete=models.CASCADE,)
    
    class Meta:
        ordering = ('course_code','name',)
    
    def _str_(self):
        return self.course_id, self.name, self.course_code, self.subaccount_id

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def get(self):
        return self.name
    
class User(PACSModel):
    canvas_id = models.IntegerField(unique = True)
    name = models.CharField(max_length = 100, null = True)
    sortable_name = models.CharField(max_length = 100, null = True)
    short_name = models.CharField(max_length = 100, null = True)
    sis_user_id = models.CharField(max_length = 100, null = True)
    login_id = models.CharField(max_length = 100)

    class Meta:
        ordering = ('sortable_name','login_id')

    def _str_(self):
        return self.login_id, self.name, self.canvas_id, self.sis_user_id  
    
    def __unicode__(self):
        return u'{0}'.format(self.sortable_name)

    def get(self):
        return self.login_id

class UserCourse(PACSModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,)
    is_teacher = models.BooleanField(default = False)

    class Meta:
        verbose_name_plural = "UserCourses"
        ordering = ('user','course')

    def _str_(self):
        return self.user, self.course  
    
    def __unicode__(self):
        return u'{0}'.format(self.user)

    def get(self):
        return self.user
       
class ActiveTerm(PACSModel):
    active_term = models.ForeignKey(Term, null=True, related_name='term', on_delete=models.CASCADE,)

    class Meta:
        ordering = ('active_term',)
        
    def _str_(self):
        return self.active_term
    
    def __unicode__(self):
        return u'{0}'.format(self.active_term)

    def get(self):
        return self.active_term
    
###########################################################
###########################################################
###########################################################
# Faculty Performance Report Tables

class TeacherWeeklyReport(ReportModel):
    usercourse = models.ForeignKey(UserCourse, on_delete=models.CASCADE,)
    
    year = models.IntegerField(null = False)
    week_number = models.IntegerField(null = False)
    
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)

    last_login = models.DateField(auto_now=False, auto_now_add=False)
    announcement_posted = models.BooleanField(default = False)
    announcement_post_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    announcement_most_recent = models.TextField()
    

    class Meta:
        verbose_name_plural = "TeacherWeeklyReports"
        ordering = ('-year', '-week_number', 'usercourse__course__name','usercourse__user__name')

    def _str_(self):
        return u'Year {0} : Week {1}'.format(self.year, self.week_number)  
    
    def __unicode__(self):
        return u'Year {0} : Week {1}'.format(self.year, self.week_number)

    def get(self):
        return self.usercourse
    
    
class TeacherWeeklyReportDiscussions(ReportModel):
    teacherweeklyreport = models.ForeignKey(TeacherWeeklyReport, on_delete=models.CASCADE,)
    discussion_id = models.IntegerField()
    discussion_name = models.CharField(max_length=200, null = True)
    due_date = models.DateField(auto_now = False, auto_now_add=False)
    unique_entry_count = models.IntegerField()
    reply_count = models.IntegerField()

    class Meta:
        verbose_name_plural = "TeacherWeeklyReportDiscussions"
        ordering = ('teacherweeklyreport','discussion_id')

    def _str_(self):
        return u'{0} - Course: {1} Disc: {1}'.format(self.teacherweeklyreport, self.teacherweeklyreport.usercourse.course.name, self.discussion_name)
    
    def __unicode__(self):
        return u'{0} - Course: {1} Disc: {1}'.format(self.teacherweeklyreport, self.teacherweeklyreport.usercourse.course.name, self.discussion_name)

    def get(self):
        return self.teacherweeklyreport
    

class TeacherWeeklyReportAssignments(ReportModel):
    teacherweeklyreport = models.ForeignKey(TeacherWeeklyReport, on_delete=models.CASCADE,)
    assignment_id = models.IntegerField()
    assignment_name = models.CharField(max_length=200, null = True)
    due_date = models.DateField(auto_now = False, auto_now_add=False)
    submission_count = models.IntegerField()
    comment_count = models.IntegerField()

    class Meta:
        verbose_name_plural = "TeacherWeeklyReportAssignments"
        ordering = ('teacherweeklyreport','assignment_id')

    def _str_(self):
        return u'{0} - Course: {1} Assn: {1}'.format(self.teacherweeklyreport, self.teacherweeklyreport.usercourse.course.name, self.assignment_name)  
    
    def __unicode__(self):
        return u'{0} - Course: {1} Assn: {1}'.format(self.teacherweeklyreport, self.teacherweeklyreport.usercourse.course.name, self.assignment_name)

    def get(self):
        return self.teacherweeklyreport
    
