from datetime import datetime, timedelta
import logging

# Nucleus Imports
from nucleus.api import CanvasAPI
from nucleus.auth import UserCredentials 
from nucleus import settings

# Model Imports
from canvas.models import Subaccount, Course, Term, User, ActiveTerm, UserCourse, TeacherWeeklyReport, TeacherWeeklyReportDiscussions, TeacherWeeklyReportAssignments
from faculty_tools.models import Submission, Assignment

def load_usercourse_data_for_term(term_id):
    if term_id is not None:
        term = Term.objects.filter(term_id = term_id).first()        
        UserCourse.objects.filter(course__term = term).delete()
        api = CanvasAPI(term_id)
        
        course_list = Course.objects.filter(term = term)
        for course in course_list:
            course_users = api.get_course_enrollments(course.course_id)
            for user in course_users:
                localuser = User.objects.filter(canvas_id = user["user_id"]).first()
                if localuser is not None:
                    isTeacher = False
                    if (user["type"] == "TeacherEnrollment"):
                        isTeacher = True 
                    usercourse_create = UserCourse.objects.create(user = localuser, course = course, is_teacher = isTeacher)
                    usercourse_create.save()
        
        
def run_teacher_weekly_report(report_date=None):
    print ("Report Date: " + str(report_date))
    
    if report_date is None:
        report_date = datetime.today()
    if type(report_date) is str:
        report_date = datetime.strptime(report_date, '%Y-%m-%d')
        
    (start_of_week, end_of_week, week_num) = getPrevWeekDateRangeFromDate(report_date)
    year = end_of_week.year
    start_of_week_str = start_of_week.strftime("%Y-%m-%d")
    end_of_week_str = end_of_week.strftime("%Y-%m-%d")
    api = CanvasAPI()
    
    # Delete existing records for this year/week
    TeacherWeeklyReport.objects.filter(year = year).filter(week_number = week_num).delete()

    print("Start of Week: " + str(start_of_week))
    print("End of Week: " + str(end_of_week))
    print("Start of Week Str: " + str(start_of_week_str))
    print("End of Week Str: " + str(end_of_week_str))
    print("Week Num: " + str(week_num))
        
    print("Current Term: " + str(api.TERM))

    term = Term.objects.filter(term_id = api.TERM).first()
    
    teachercourse_list = UserCourse.objects.filter(course__term = term).filter(is_teacher = True)
    for teachercourse in teachercourse_list:
        #teacher_weekly_report = TeacherWeeklyReport.objects.create()
        canvas_user_details = api.get_user_details(teachercourse.user.canvas_id)
        last_login = datetime.strptime(canvas_user_details["last_login"], '%Y-%m-%dT%H:%M:%SZ')
        
        announcements = api.get_course_announcements_for_date_range_by_teacher(teachercourse.course.course_id, teachercourse.user.canvas_id, start_of_week_str, end_of_week_str)
        num_announcements = len(announcements)
        #print ("TeacherCourse: CourseID:" + str(teachercourse.course) + " Announcements: " + str(num_announcements) + " LastLogin: " + str(last_login))
        if num_announcements > 0:
            counter = 0
            announcement_posted = True
            most_recent_announcement_date = datetime.strptime(announcements[counter]["posted_at"], '%Y-%m-%dT%H:%M:%SZ')
            most_recent_announcement_content = announcements[counter]["message"]
            for announcement in announcements:
                current_date = datetime.strptime(announcement["posted_at"], '%Y-%m-%dT%H:%M:%SZ')
                current_content = announcement["message"]
                if current_date > most_recent_announcement_date:
                    most_recent_announcement_date = current_date
                    most_recent_announcement_content = current_content
                counter = counter + 1
            #print ("Announcement Posted Date: " + str(most_recent_announcement_date))
            #print ("Announcement Posted Date: " + str(most_recent_announcement_date) + " Content: " + str(most_recent_announcement_content))
        else:
            announcement_posted = False
            #print ("No Announcements Posted")
            
        if announcement_posted:
            teacherweeklyreportrecord = TeacherWeeklyReport.objects.create(usercourse = teachercourse, start_date = start_of_week, end_date = end_of_week, year = year, week_number = week_num, last_login = last_login, announcement_posted = announcement_posted, announcement_post_date = most_recent_announcement_date, announcement_most_recent = most_recent_announcement_content)
        else:
            teacherweeklyreportrecord = TeacherWeeklyReport.objects.create(usercourse = teachercourse, start_date = start_of_week, end_date = end_of_week, year = year, week_number = week_num, last_login = last_login, announcement_posted = announcement_posted)
            
        teacherweeklyreportrecord.save()
        get_teacher_weekly_report_assignments(teacherweeklyreportrecord)
        get_teacher_weekly_report_discussions(teacherweeklyreportrecord)
        
        #print (str(teachercourse.course.course_id) + " - Announcements: " + str(announcements))
        #print("TeacherCourse Record: " + str(teachercourse))

def get_teacher_weekly_report_assignments(teacherweeklyreportrecord):
    
    start_date = teacherweeklyreportrecord.start_date
    end_date = teacherweeklyreportrecord.end_date
    course_id = teacherweeklyreportrecord.usercourse.course.course_id
    teacher_id = teacherweeklyreportrecord.usercourse.user.canvas_id
    
    api = CanvasAPI()
    
    assignments = api.get_online_upload_assignments_with_due_date_in_range( course_id, start_date, end_date)
    for assignment in assignments:
        assignment_id = assignment["id"]
        assignment_name = assignment["name"].encode('ascii', 'ignore')
        due_date = datetime.strptime(assignment["due_at"], '%Y-%m-%dT%H:%M:%SZ')
        
        print ("Assignment: " + assignment_name)
        
        submissions = api.get_assignment_submissions(course_id, assignment_id)
        submission_counter = 0
        comment_counter = 0
        for submission in submissions:
            submission_counter = submission_counter + 1
            submission_comments = submission["submission_comments"]
            for submission_comment in submission_comments:
                if submission_comment["comment"] is not None and submission_comment["author_id"] == teacher_id:
                    comment_counter = comment_counter + 1
                    #print ("Comment Counter: " + str(comment_counter))
                    
        teacherweeklyreportassignmentsrecord = TeacherWeeklyReportAssignments.objects.create(teacherweeklyreport = teacherweeklyreportrecord, assignment_id = assignment_id, assignment_name = assignment_name, due_date = due_date, submission_count = submission_counter, comment_count = comment_counter)
        teacherweeklyreportassignmentsrecord.save()

        
def get_teacher_weekly_report_discussions(teacherweeklyreportrecord):

    start_date = teacherweeklyreportrecord.start_date
    end_date = teacherweeklyreportrecord.end_date
    course_id = teacherweeklyreportrecord.usercourse.course.course_id
    teacher_id = teacherweeklyreportrecord.usercourse.user.canvas_id
    
    api = CanvasAPI()
    
    discussions = api.get_course_discussions_with_due_date_in_range(course_id, start_date, end_date)
    for discussion in discussions:
        discussion_id = discussion["id"]
        discussion_name = discussion["title"].encode('ascii', 'ignore')
        due_date = datetime.strptime(discussion["assignment"]["due_at"], '%Y-%m-%dT%H:%M:%SZ')
        
        print ("Discussions: " + discussion_name)
        
        discussion_all_views = api.get_course_discussion_full(course_id, discussion_id)
        views = discussion_all_views["view"]
        
        top_level_reply_counter = 0
        reply_counter = 0
        for view in views:
            #print ("Current Submission: " + str(submission))
            top_level_reply_counter = top_level_reply_counter + 1
            if view.has_key("replies"):
                replies = view["replies"]
                for reply in replies:
                    if reply.has_key("user_id"):
                        if reply["user_id"] == teacher_id:
                            reply_counter = reply_counter + 1
                            #print ("Reply Counter: " + str(reply_counter))
                            break
                    
        teacherweeklyreportdiscussionsrecord = TeacherWeeklyReportDiscussions.objects.create(teacherweeklyreport = teacherweeklyreportrecord, discussion_id = discussion_id, discussion_name = discussion_name, due_date = due_date, unique_entry_count = top_level_reply_counter, reply_count = reply_counter)
        teacherweeklyreportdiscussionsrecord.save()


def getPrevWeekDateRangeFromDate(date_obj):
    start_of_week = date_obj - timedelta(days=date_obj.weekday()+7)  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    week_num = start_of_week.strftime("%U")
    return start_of_week, end_of_week, week_num
