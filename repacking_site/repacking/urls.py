from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('repacking/history/', views.history),
    path('repacking/standards/', views.show_standards),
    path('repacking/standards/new/', views.make_new_standard),
    path('repacking/sku/', views.show_standards),
    path('repacking/start/', views.start,  name='start'),
    path('repacking/sku/export/', views.sku_export),
    path('repacking/history/export/', views.history_export),
    path('repacking/delete/<str:sku_code>/', views.delete),
    path('repacking/<str:sku_code>/', views.detail),
    path('repacking/<str:sku_code>/<str:idp_code>/<str:operators>/repack_finished', views.finish),
    path('repacking/<str:sku_code>/<str:idp_code>/<str:operators>/repack_paused', views.pause),
    path('repacking/<str:sku_code>/<str:idp_code>/<str:operators>/repack_cancelled', views.cancel),
    path('repacking/<str:sku_code>/<str:idp_code>/<str:operators>/', views.repacking),


]
