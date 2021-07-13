from datetime import datetime, timedelta
from nucleus.api import CanvasAPI
from canvas.cron import *

# Steps to run:
# 1. su - pacs-portal_rpoject
# 2. python manage.py shell
# 3. execfile('cron/twr_manual.py')

# Each of these lines runs the report for the previous week given the date specified
run_teacher_weekly_report(datetime.strptime("2021-02-02", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-02-09", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-02-16", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-02-23", "%Y-%m-%d"))

run_teacher_weekly_report(datetime.strptime("2021-01-05", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-01-12", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-01-19", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-01-26", "%Y-%m-%d"))

run_teacher_weekly_report(datetime.strptime("2021-03-02", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-03-09", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-03-16", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-03-23", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-03-30", "%Y-%m-%d"))

run_teacher_weekly_report(datetime.strptime("2021-04-06", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-04-13", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-04-20", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-04-27", "%Y-%m-%d"))

run_teacher_weekly_report(datetime.strptime("2021-05-04", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-05-11", "%Y-%m-%d"))
run_teacher_weekly_report(datetime.strptime("2021-05-18", "%Y-%m-%d"))

