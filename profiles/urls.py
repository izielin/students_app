from django.urls import include, path

from . import views

urlpatterns = [
    path('list/', views.ProfileListView.as_view(), name='profile_changelist'),
    path('add/', views.ProfileCreateView.as_view(), name='profile_add'),
    path('change/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_change'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]
