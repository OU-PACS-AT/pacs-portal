from toolkit.helpers.admin import auto_admin_register
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
import logging

# Nucleus Imports
from nucleus.api import CanvasAPI
from nucleus.auth import UserCredentials 
from nucleus import settings

# Model Imports
from models import Subaccount, Course, Term, User, ActiveTerm, UserCourse
from models import TeacherWeeklyReport, TeacherWeeklyReportDiscussions, TeacherWeeklyReportAssignments
from faculty_tools.models import Submission, Assignment

class TermAdmin(admin.ModelAdmin):
    list_display = ('term_id', 'name')

class ActiveTermAdmin(admin.ModelAdmin):
    list_display = ('active_term', )


class SubaccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'subaccount_id', 'parent')
    change_list_template = 'admin/subaccount_change_list.html'
    
    def get_urls(self):
        super_urls = super(SubaccountAdmin, self).get_urls()
        custom_urls = [
            url('reload/$', self.reload_subaccounts)
        ]
        return custom_urls + super_urls
    
    def changelist_view(self, request, extra_context = None):
        extra_context = extra_context or {}
        most_recent_timestamp = self.model.objects.all().order_by('created_at').first()
        if most_recent_timestamp is not None:
            extra_context['load_date'] = most_recent_timestamp.created_at
        return super(SubaccountAdmin, self).changelist_view(request, extra_context=extra_context)
    
    def reload_subaccounts(self, request):
        self.model.objects.all().delete()
        creds = UserCredentials()
        api = CanvasAPI()
        
        first_iteration = api.get_subaccounts()
        for sub_account in first_iteration:
            sub_account_create = self.model.objects.create(subaccount_id = sub_account['id'], name = sub_account['name'])
            sub_account_create.save()
    
        second_iteration = api.get_subaccounts()
        for sub_account in second_iteration:
            sub_account_parent = self.model.objects.filter(subaccount_id = sub_account['parent_account_id']).first()
            sub_account_child = self.model.objects.filter(subaccount_id = sub_account['id']).first()
            sub_account_child.parent = sub_account_parent
            sub_account_child.save()
            
        self.message_user(request, "Subaccounts successfully reloaded!")
        return HttpResponseRedirect("../")


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_code', 'course_id', 'subaccount', 'term']
    change_list_template = 'admin/course_change_list.html'
    
    def get_urls(self):
        super_urls = super(CourseAdmin, self).get_urls()
        custom_urls = [
            url(r'(?P<term_id>.+)/reload/$', self.reload_course)
        ]
        return custom_urls + super_urls

    def changelist_view(self, request, extra_context = None):
        extra_context = extra_context or {}
        most_recent_timestamp = self.model.objects.all().order_by('created_at').first()
        if most_recent_timestamp is not None:
            extra_context['load_date'] = most_recent_timestamp.created_at
            
        api = CanvasAPI()
        extra_context['terms'] = Term.objects.all()
        extra_context['current_term_id'] = api.TERM
        return super(CourseAdmin, self).changelist_view(request, extra_context = extra_context)

    def reload_course(self, request, term_id):
        term = Term.objects.filter(term_id = term_id).first()        
        self.model.objects.filter(term = term).delete()
        creds = UserCredentials()
        api = CanvasAPI(term = term_id)
        
        course_list = api.get_courses_by_term()
        for course in course_list:
            subaccount = Subaccount.objects.filter(subaccount_id = course['account_id']).first()
            self.model.objects.filter(course_id = course['id']).delete()
            course_create = self.model.objects.create(course_id = course['id'], name = course['name'], course_code = course['course_code'], term = term, subaccount = subaccount)
            course_create.save()
            
        self.message_user(request, "Course list successfully reloaded!")
        return HttpResponseRedirect("../../")
    
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'login_id', 'canvas_id', 'sis_user_id']
    change_list_template = 'admin/user_change_list.html'
    
    def get_urls(self):
        super_urls = super(UserAdmin, self).get_urls()
        custom_urls = [
            url(r'reload/$', self.reload_user)
        ]
        return custom_urls + super_urls

    def changelist_view(self, request, extra_context = None):
        extra_context = extra_context or {}
        most_recent_timestamp = self.model.objects.all().order_by('created_at').first()
        if most_recent_timestamp is not None:
            extra_context['load_date'] = most_recent_timestamp.created_at
        return super(UserAdmin, self).changelist_view(request, extra_context=extra_context)

    def reload_user(self, request):
        #self.model.objects.all().delete()
        Submission.objects.all().delete()
        creds = UserCredentials()
        api = CanvasAPI()
        
        user_list = api.get_account_users()
        for user in user_list:
            userRecord = self.model.objects.filter(canvas_id = user['id']).first()
            if userRecord is None:
                user_create = self.model.objects.create(canvas_id = user['id'], name = user['name'], sortable_name = user['sortable_name'], short_name = user['short_name'], sis_user_id = user['sis_user_id'], login_id = user['login_id']) 
                user_create.save()
            
        self.message_user(request, "Canvas User list successfully reloaded!")
        return HttpResponseRedirect("../")

class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_teacher')
    change_list_template = 'admin/usercourse_change_list.html'
    
    def get_urls(self):
        super_urls = super(UserCourseAdmin, self).get_urls()
        custom_urls = [
            url(r'(?P<term_id>.+)/reload/$', self.reload_usercourse)
        ]
        return custom_urls + super_urls

    def changelist_view(self, request, extra_context = None):
        extra_context = extra_context or {}
        most_recent_timestamp = self.model.objects.all().order_by('created_at').first()
        if most_recent_timestamp is not None:
            extra_context['load_date'] = most_recent_timestamp.created_at
            
        api = CanvasAPI()
        extra_context['terms'] = Term.objects.all()
        extra_context['current_term_id'] = api.TERM
        return super(UserCourseAdmin, self).changelist_view(request, extra_context = extra_context)

    def reload_usercourse(self, request, term_id):
        term = Term.objects.filter(term_id = term_id).first()        
        #self.model.objects.filter(course__term = term).delete()
        creds = UserCredentials()
        api = CanvasAPI(term = term_id)
        
        course_list = Course.objects.filter(term = term)
        for course in course_list:
            course_users = api.get_course_enrollments(course.course_id)
            for user in course_users:
                localuser = User.objects.filter(canvas_id = user["user_id"]).first()
                if localuser is not None:
                    isTeacher = False
                    if (user["type"] == "TeacherEnrollment"):
                        isTeacher = True
                        
                    usercourse_record = self.model.objects.filter(user = localuser, course = course).first()
                    if usercourse_record is None: 
                        #logging.warning("Creating UserCourse record for: " + str(localuser))
                        usercourse_create = self.model.objects.create(user = localuser, course = course, is_teacher = isTeacher)
                        usercourse_create.save()
                    else:
                        usercourse_record.is_teacher = isTeacher
                        usercourse_record.save()
            
        self.message_user(request, "User Course (Enrollments) list successfully reloaded!")
        return HttpResponseRedirect("../../")

class TeacherWeeklyReportAdmin(admin.ModelAdmin):
    list_display = ('_teacher_weekly_report', '_course_name', '_teacher_name', 'start_date', 'end_date', 'last_login', 'announcement_posted', 'announcement_post_date')
    list_filter =('year', 'week_number', 'usercourse__user')
    ordering = ('year', 'week_number', 'usercourse__course__name', 'usercourse__user__name')
    
    #search_fields = ["usercourse__course__name", "usercourse__user__name", "year", "week"]
    search_fields = ["usercourse__course__name", "usercourse__user__name"]
    
    def _teacher_weekly_report(self, obj):
        return u'Year: {0} Week: {1}'.format(obj.year, obj.week_number)

    def _course_name(self, obj):
        return obj.usercourse.course.name
    
    def _teacher_name(self, obj):
        return obj.usercourse.user.name

class TeacherWeeklyReportDiscussionsAdmin(admin.ModelAdmin):
    list_display = ('_teacher_weekly_report', '_course_name', '_teacher_name', 'discussion_id', 'discussion_name', 'due_date', 'unique_entry_count', 'reply_count')
    list_filter = ('teacherweeklyreport__year', 'teacherweeklyreport__week_number')
    ordering = ('teacherweeklyreport__year', 'teacherweeklyreport__week_number', 'teacherweeklyreport__usercourse__course__name', 'teacherweeklyreport__usercourse__user__name')

    search_fields = ["teacherweeklyreport__usercourse__course__name", "teacherweeklyreport__usercourse__user__name"]

    def _teacher_weekly_report(self, obj):
        return u'Year: {0} Week: {1}'.format(obj.teacherweeklyreport.year, obj.teacherweeklyreport.week_number)
    
    def _course_name(self, obj):
        return obj.teacherweeklyreport.usercourse.course.name
    
    def _teacher_name(self, obj):
        return obj.teacherweeklyreport.usercourse.user.name
    
    def _week_num(self, obj):
        return obj.teacherweeklyreport.week_number
    
class TeacherWeeklyReportAssignmentsAdmin(admin.ModelAdmin):
    list_display = ('_teacher_weekly_report', '_course_name', '_teacher_name', 'assignment_id', 'assignment_name', 'due_date', 'submission_count', 'comment_count')
    list_filter = ('teacherweeklyreport__year', 'teacherweeklyreport__week_number')
    ordering = ('teacherweeklyreport__year', 'teacherweeklyreport__week_number', 'teacherweeklyreport__usercourse__course__name', 'teacherweeklyreport__usercourse__user__name')

    search_fields = ["teacherweeklyreport__usercourse__course__name", "teacherweeklyreport__usercourse__user__name"]

    def _teacher_weekly_report(self, obj):
        return u'Year: {0} Week: {1}'.format(obj.teacherweeklyreport.year, obj.teacherweeklyreport.week_number)
    
    def _course_name(self, obj):
        return obj.teacherweeklyreport.usercourse.course.name
    
    def _teacher_name(self, obj):
        return obj.teacherweeklyreport.usercourse.user.name
    
    def _week_num(self, obj):
        return obj.teacherweeklyreport.week_number

admin.site.register(TeacherWeeklyReport, TeacherWeeklyReportAdmin)
admin.site.register(TeacherWeeklyReportDiscussions, TeacherWeeklyReportDiscussionsAdmin)
admin.site.register(TeacherWeeklyReportAssignments, TeacherWeeklyReportAssignmentsAdmin)

admin.site.site_header = "Pacs-Portal Admin Panel"

admin.site.register(Subaccount, SubaccountAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(ActiveTerm, ActiveTermAdmin)        
admin.site.register(User, UserAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
