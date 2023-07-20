# snippets/urls.py
from django.urls import path
from loader import views

urlpatterns = [
    path('', views.api_root),
    path("datafiles/", views.DataFileAPIView.as_view(), name='datafile-list'),
    path("datafiles/<int:pk>/", views.DataFileDetail.as_view(), name='datafile-detail'),
    path('projects/', views.ProjectList.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project-detail'),
]