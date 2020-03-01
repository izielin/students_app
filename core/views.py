from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.http import JsonResponse
from django.views.generic import CreateView
from .forms import StudentSignUpForm, TeacherSignUpForm
from projects.models import Project
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from .decorators import anonymous_required
from django.utils.decorators import method_decorator

User = get_user_model()


def home(request):
    global User
    count = User.objects.count()
    context = {
        'count': count,
    }

    if request.user.is_authenticated:
        projects = Project.objects.filter(teacher=request.user)
        context['projects'] = projects

    return render(request, 'core/home.html', context)


def signup_page(request):
    return render(request, 'registration/signup.html')


def create_account(self, form):
    user = form.save(commit=False)
    user.is_active = False
    user.save()
    current_site = get_current_site(self.request)
    mail_subject = 'Activate your account.'
    message = render_to_string('core/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = form.cleaned_data.get('email')
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    messages.info(self.request, 'Please confirm your email address to complete the registration')
    return render(self.request, 'core/messages.html')


@method_decorator(anonymous_required, name='dispatch')
class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form, **kwargs):
        return create_account(self, form)


@method_decorator(anonymous_required, name='dispatch')
class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form, **kwargs):
        return create_account(self, form)


def validate_username_or_email(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    data = {
        'username_is_taken': User.objects.filter(username__iexact=username).exists(),
        'email_is_taken': User.objects.filter(email__iexact=email).exists()
    }
    if data['username_is_taken']:
        data['username_error_message'] = 'A user with this username already exists.'
    if data['email_is_taken']:
        data['email_error_message'] = 'A user with this email already exists.'
    return JsonResponse(data)


def activate(request, uidb64, token):
    global User
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')
