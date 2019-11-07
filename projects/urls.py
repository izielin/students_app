from django.urls import path
from . import views

urlpatterns = [
    path('project/<int:pk>', views.projects, name='project'),
    path('project/list/', views.projects_list, name='project_list'),
    path('project/add/', views.ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/edit', views.ProjectUpdateView.as_view(), name='project_change'),
    path('course/add/', views.CourseCreateView.as_view(), name='course_add'),

]

