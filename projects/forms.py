from django import forms
from .models import Project, Course, Document
from .widgets import FengyuanChenDatePickerInput


class ProjectForm(forms.ModelForm):
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


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'document']