from django.urls import path

from . import views

app_name = "timer"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>/<int:count>/", views.sleeping, name="sleeping"),
    path("upload/", views.upload_file, name="upload_file")
]
