from django.urls import path
from . import views

urlpatterns = [
    path('project/<int:pk>', views.projects, name='project'),
    path('project/list/', views.projects_list, name='project_list'),
    path('project/add/', views.ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/delete', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/edit', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<int:pk>/add', views.CourseCreateView.as_view(), name='course_add'),
    path('course/<int:pk>/edit', views.CourseUpdateView.as_view(), name='course_edit'),
    path('course/<int:pk>/delete', views.CourseDeleteView.as_view(), name='course_delete'),
    path('course/<int:pk>', views.course, name='course'),
    path('course/<int:pk>/upload', views.upload, name='course_upload'),
    path('upload/<int:pk>', views.UploadDeleteView.as_view(), name='upload_delete'),
]

