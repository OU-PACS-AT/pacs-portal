from django import forms
from toolkit.forms import CCESimpleSearchForm, CCEModelSearchForm, CCEModelForm

from scaffold.models import Course, Assignment


class CourseSimpleSearch(CCESimpleSearchForm):
    search_placeholder = 'Search Courses'

    class Meta(CCESimpleSearchForm.Meta):
        model = Course
        field_lookups = {'search': ('id__icontains',
                                    'name__icontains')}
        
        
class AssignmentDatesForm(forms.ModelForm): 
    
    class Meta:
        model = Assignment
        fields = [
        'assignment_name',
        'start_date',
        'due_date',
        'end_date',
        ]
             
        widgets = { 'assignment_name' :forms.TextInput(attrs={'readonly':'readonly', 'class' : 'grey-text', 'size' : '25'}),
                    'start_date' : forms.DateInput(format = '%m/%d/%Y', attrs ={ 'class' : 'datepicker'}),
                    'due_date' : forms.DateInput(format = '%m/%d/%Y', attrs ={ 'class' : 'datepicker' }),
                    'end_date' : forms.DateInput(format = '%m/%d/%Y', attrs ={ 'class' : 'datepicker' }),}
        
    class Media:
        css = {'assignment_name': ('changeDates.css',)} 
        
        
AssignmentDatesFormSet = forms.modelformset_factory(
    model = Assignment,
    form = AssignmentDatesForm,
    extra = 0,
    ) 