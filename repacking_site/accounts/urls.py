from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='profile.html')),
    path('profile/', views.profile),
    path('user_list/', views.user_list),
    path('', include('django.contrib.auth.urls')),
]


