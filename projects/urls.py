from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('projects/', views.projects, name = "projects"),
    path("project/<str:pk>/", views.project, name = "project"),
    path('create project/', views.create_project, name = "create-project"),
    path("edit project/<str:pk>/", views.editProject, name = "update-project"),
    path("remove project/<str:pk>/", views.removeProject, name = "delete-project"),
]