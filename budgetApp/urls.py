from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('budget/projects/', views.project_list, name='list'),
    path('budget/projects/add/', views.ProjectCreateView.as_view(), name='add'),
    #path('budget/projects/create/', views.create_project, name='create'),
    path('budget/projects/<slug:project_slug>/', views.project_detail, name='detail'),
]
