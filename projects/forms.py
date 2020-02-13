from django import forms
from .models import Project, Course, File, Mark
from .widgets import FengyuanChenDatePickerInput
from profiles.models import Profile
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


class TakePartForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['projects']
        widgets = {'projects': forms.HiddenInput()}


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('course', 'student', 'mark',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MarkForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = Profile.objects.none()
        if 'course' in self.data:
            try:
                course_data = int(self.data.get('course'))
                self.fields['student'].queryset = Profile.objects.filter(projects__course__id=course_data).order_by('last_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['student'].queryset = self.instance.profile.projects_set.order_by('first_name')
