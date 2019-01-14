from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

import logging

from datetime import date
#from splitjson.widgets import SplitJSONWidget
from .models import CanvasAssignment
from .models import CanvasClass
from .models import CanvasStudent


class GetClassNumber(forms.Form):
    classNumber = forms.CharField(label = 'URL', widget=forms.TextInput(attrs={'placeholder': 'Paste URL here', 'size' : '50'}))
    
class SelectClass(forms.ModelForm):
    class Meta:
        model = CanvasClass
        fields = [
        'class_name',
        ]
    class_name = forms.ModelChoiceField(queryset=CanvasClass.objects.all(),label = "Choose Class")
	
class TableForm(forms.ModelForm):
    
    class Meta:
        model = CanvasAssignment
        fields = [
    	
	    'assignment_name',
        'start_date',
        'due_date',
        'end_date',
        ]
             
        widgets = { 'assignment_name' :forms.TextInput(attrs={'readonly':'readonly', 'class' : 'inputA', 'size' : '25'}),
                    'start_date' : forms.DateInput(format = '%m/%d/%Y', attrs ={ 'class' : 'datepicker'}),
                    'due_date' : forms.DateInput(format = '%m/%d/%Y', attrs ={ 'class' : 'datepicker' }),
                    'end_date' : forms.DateInput(format = '%m/%d/%Y', attrs ={ 'class' : 'datepicker' }),}
        
    class Media:
        css = {'assignment_name': ('changeDates.css',)} 
        
        
TableFormSet = forms.modelformset_factory(
    model = CanvasAssignment,
    form = TableForm,
    extra = 0,
    ) 
        
        
class StudentForm(forms.ModelForm):
    #checked = forms.BooleanField(required=False) 
    
    class Meta:
        model = CanvasStudent
        fields = [        
    #    'student_id',
        'student_name',
    #    'checked',
        ]
        
    student_name = forms.ModelChoiceField(queryset=CanvasStudent.objects.all(),label = "Choose Student")    
    
    
class XAssignmentForm(forms.ModelForm): 
    
    class Meta:
        model = CanvasAssignment
        fields = [        
        'assignment_name',
        'due_date',
        ]
            
    assignment_name = forms.ModelChoiceField(queryset=CanvasAssignment.objects.all(),label = "Choose Assignment")
    

class XTableForm(forms.ModelForm): 
    
    class Meta:
        model = CanvasAssignment
        fields = [        
        'assignment_name',
        'due_date',
        ]
             
        widgets = { 'assignment_name' :forms.TextInput(attrs={'readonly':'readonly', 'class' : 'grey-text', 'size' : '25'}),                    
                    'due_date' : forms.DateInput(format = '%m-%d-%Y', attrs ={ 'class' : 'datepicker' }),}
        
    class Media:
        css = {'assignment_name': ('changeDates.css',)} 
            
        
XTableFormSet = forms.modelformset_factory(
    model = CanvasAssignment,
    form = XTableForm,
    extra = 0,
    ) 
 

class ConfirmForm(forms.Form):
    pass

class SavedForm(forms.Form):
    pass
 

   


