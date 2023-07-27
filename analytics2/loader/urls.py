# snippets/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from loader import views

urlpatterns = [
    path('', views.api_root),
    path("datafiles/<int:pk>/", views.DataFileDetail.as_view(), name='datafile-detail'),
    path('projects/', views.ProjectList.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project-detail'),
    path('projects/<int:project_fk>/<str:year_quarter>/', views.DataFileAPIView.as_view(), name='datafile-list'),
]