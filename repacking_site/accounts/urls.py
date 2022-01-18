from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html')),
    path('profile/', views.profile),
    path('user_list/', views.users_list),
    path('user_list/export/', views.export_users),
    path('add_user/', views.add_user),
    path('groups_list/', views.groups_list),
    path('groups_list/export/', views.export_groups),
    path('', include('django.contrib.auth.urls')),
]
