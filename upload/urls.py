from django.urls import path
from . import views

urlpatterns = [
    path('clear/', views.clear_database, name='clear_database'),
    path('basic-upload/', views.BasicUploadView.as_view(), name='basic_upload'),

]
