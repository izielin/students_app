from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


def anonymous_required(function=None, redirect_url=None):
    '''
    Decorator for views that checks that the user isn't logged,
    redirects to the home page if necessary.
    '''
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def student_required(function):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''

    def _function(request, *args, **kwargs):
        if not request.user.is_student:
            messages.info(request, 'Access restricted, for students only')
            return HttpResponseRedirect(reverse('login'))
        return function(request, *args, **kwargs)

    return _function


def teacher_required(function):
    '''
        Decorator for views that checks that the logged in user is a teacher,
        redirects to the log-in page if necessary.
        '''
    def _function(request, *args, **kwargs):
        if not request.user.is_teacher:
            messages.info(request, 'Access restricted, for teachers only')
            return HttpResponseRedirect(reverse('login'))
        return function(request, *args, **kwargs)

    return _function
