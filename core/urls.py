from django.urls import path, include
from . import views
from django.conf.urls import url
   
urlpatterns = [
    path('', views.home, name='home'),
    url(r'^signup/$', views.signup_page, name='signup'),
    path('accounts/signup/student/', views.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', views.TeacherSignUpView.as_view(), name='teacher_signup'),
    url(r'^ajax/validate_username/$', views.validate_username_or_email, name='validate_username_or_email'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate')
   ]