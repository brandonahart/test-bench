from django.urls import path
from . import views

app_name = 'sleep'
urlpatterns = [
    path('', views.sleeping_time, name='sleeping_time'),
    path('list/', views.sleeping_list, name='sleeping_list'),
]
