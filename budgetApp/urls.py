from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('budget/projects/', views.project_list, name='list'),
    path('budget/projects/reports', views.project_report, name='reports'),
    path('budget/projects/add/', views.ProjectCreateView.as_view(), name='add'),
    #path('projects/<slug:project_slug>/delete/', views.delete_project, name='delete'),
    path('budget/projects/<slug:project_slug>/delete/', views.delete_project, name='delete'),
    #path('budget/projects/create/<slug:project_slug>/', views.add_expense, name='create'),
    path('budget/projects/<slug:project_slug>/', views.project_detail, name='detail'),
    path('budget/projects/income/', views.income_list, name='income-list'),
    path('budget/projects/income/create/', views.income_create, name='income-create'),
    path('budget/projects/income/<int:pk>/update/', views.income_edit, name='income-update'),
    path('budget/projects/income/<int:pk>/delete/', views.income_delete, name='income-delete'),
]
