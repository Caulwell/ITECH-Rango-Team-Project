from django.urls import path
from rango import views

app_name='rango'

urlPatterns = [
    path('', views.index, name='index'),
]