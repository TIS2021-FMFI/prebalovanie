from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='detail'),
	path('history/', views.history, name='detail'),
	path('standards/', views.index, name='index'),
	path('<str:sku_code>/', views.detail, name='detail'),
	path('<str:sku_code>/repack_finished', views.finish, name='detail'),
]