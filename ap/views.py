from django.shortcuts import render

# Toolkit imports
from toolkit.views import  CCETemplateView


class NewCourseRequests(CCETemplateView):
    sidebar_group = ['ap', 'new_course_requests']
    template_name = 'new_course_requests.html'
    page_title = 'New Course Requests'    
       
class ReviseCourseRequests(CCETemplateView):
    sidebar_group = ['ap', 'revise_course_requests']
    template_name = 'revise_course_requests.html'
    page_title = 'Revise Course Requests'  
    
class TextbookChangeRequests(CCETemplateView):
    sidebar_group = ['ap', 'textbook_change_requests']
    template_name = 'textbook_change_requests.html'
    page_title = 'Textbook Change Requests'  
    
class AcceptanceDeclarations(CCETemplateView):
    sidebar_group = ['ap', 'acceptance_declarations']
    template_name = 'acceptance_declarations.html'
    page_title = 'Acceptance Declarations'  
    
class RedevelopCourseRequests(CCETemplateView):
    sidebar_group = ['ap', 'redevelop_course_requests']
    template_name = 'redevelop_course_requests.html'
    page_title = 'Re-develop Course Requests'  