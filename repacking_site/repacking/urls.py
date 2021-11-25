from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('repacking/history/', views.history),
    path('repacking/standards/', views.index),
    path('repacking/standards/new/', views.make_new_standard),
    path('repacking/<str:sku_code>/', views.detail),
    path('repacking/<str:sku_code>/repack_finished', views.finish)
]
