from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/list/', views.profiles_list, name='profile_changelist'),
    path('profile/<int:pk>/edit', views.ProfileUpdateView.as_view(), name='profile_change'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]

