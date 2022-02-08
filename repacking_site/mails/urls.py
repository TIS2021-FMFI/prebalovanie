from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index),
    path("send/", views.send),
    path('delete/<str:mail>/', views.delete),
]
