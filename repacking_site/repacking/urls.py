from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('repacking/history/', views.history),
    path('repacking/standards/', views.index),
    path('repacking/standards/new/', views.make_new_standard),
    path('repacking/<str:sku_code>/repack_finished', views.finish),
    path('repacking/<str:sku_code>/repack_paused', views.pause),
    path('repacking/<str:sku_code>/repack_cancelled', views.cancel),
    path('repacking/<str:sku_code>/', views.detail),

    path('repacking/sku', views.show_standards),
]
