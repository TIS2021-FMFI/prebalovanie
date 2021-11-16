from django.urls import path
from . import views

urlpatterns = [
    path('mails/index/', views.index),
]
