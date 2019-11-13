from django.urls import path, include
from . import views
from django.conf.urls import url
   
urlpatterns = [
    path('', views.home, name='home'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', views.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', views.TeacherSignUpView.as_view(), name='teacher_signup'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    path('secret/', views.secret_page, name='secret'),
    path('secret2/', views.SecretPage.as_view(), name='secret2'),
    path('accounts/', include('django.contrib.auth.urls'))
   ]