from django import forms
from toolkit.forms import CCESimpleSearchForm, CCEModelSearchForm, CCEModelForm

from resources.models import CourseChangeRequest


class CourseChangeRequestForm(CCEModelForm):
    class Meta:
        model = CourseChangeRequest
        fields = ('name',
                  'description',
                  'course_id',
                  'approved',
                  )
