from django.urls import path
from . import views

urlpatterns = [
    path('logs/index/', views.index),
]
