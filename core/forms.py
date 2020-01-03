from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False, *args, **kwargs)
        user.is_student = True
        user.save()
        return user


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False, *args, **kwargs)
        user.is_teacher = True
        user.save()
        return user