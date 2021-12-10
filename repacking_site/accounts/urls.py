from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html')),
    path('profile/', views.profile),
    path('', include('django.contrib.auth.urls')),
]

