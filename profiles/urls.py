from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/list/', views.ProfileListView.as_view(), name='profile_changelist'),
    path('profile/add/', views.ProfileCreateView.as_view(), name='profile_add'),
    path('profile/change/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_change'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]

