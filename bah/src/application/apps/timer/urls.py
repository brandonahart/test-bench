from django.urls import path

from . import views

app_name = 'timer'
urlpatterns = [
    path("", views.index, name="index"),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list')
]
