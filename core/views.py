from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import UserRegisterForm
from django.views.generic import CreateView
from profiles.models import Profile


def home(request):
    count = User.objects.count()
    return render(request, 'core/home.html', {'count': count})


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserRegisterForm
    
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
