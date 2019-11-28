from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.http import JsonResponse
from .forms import UserRegisterForm
from django.views.generic import CreateView
from .forms import StudentSignUpForm, TeacherSignUpForm


def home(request):
    count = User.objects.count()
    return render(request, 'core/home.html', {'count': count})


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserRegisterForm
    
    def get_success_url(self):
         return reverse('login')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def get_success_url(self):
         return reverse('login')


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def get_success_url(self):
         return reverse('login')


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)


@login_required
def secret_page(request):
    return render(request, 'core/secret_page.html')


class SecretPage(LoginRequiredMixin, TemplateView):
    template_name = 'core/secret_page.html'
