from django import forms
from .models import Project, Course, File
from .widgets import FengyuanChenDatePickerInput
from .models import File
from bootstrap_modal_forms.forms import BSModalForm

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)


class ProjectForm(BSModalForm):
    class Meta:
        model = Project
        fields = ['name', 'summary']


class CourseForm(forms.ModelForm):
    end_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=FengyuanChenDatePickerInput()
    )

    class Meta:
        model = Course
        fields = ['name', 'summary', 'end_date', 'credits', 'mandatory', 'year']
