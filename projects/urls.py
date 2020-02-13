from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('project/<int:pk>', views.projects, name='project'),
    url(r'^project/details/(?P<pk>\d+)/$', views.ProjectReadView.as_view(), name='project_shortcut'),
    path('project/list/', views.projects_list, name='project_list'),
    path('project/list/student', views.projects_list_for_students, name='s_project_list'),
    path('project/add/', views.ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/delete', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/edit', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<int:pk>/add', views.CourseCreateView.as_view(), name='course_add'),
    path('course/<int:pk>/edit', views.CourseUpdateView.as_view(), name='course_edit'),
    path('course/<int:pk>/delete', views.CourseDeleteView.as_view(), name='course_delete'),
    path('course/<int:pk>', views.CourseView.as_view(), name='course'),
    path('upload/<int:pk>', views.delete_file, name='upload_delete'),
    path('course/<int:pk>/setmark/', views.MarkCreateView.as_view(), name='mark'),
    path('ajax/load-students/', views.load_students, name='ajax_load_students'),

]

