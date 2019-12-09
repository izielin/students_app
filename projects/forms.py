from django import forms
from .models import Project, Course, Mark


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'summary']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'summary', 'start_date', 'end_date', 'credits', 'mandatory', 'year']


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = '__all__'
