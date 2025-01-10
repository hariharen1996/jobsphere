from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from . import api_views

urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('register/',views.user_register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.user_profile,name='profile'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('api/login-api/',api_views.login_view,name='login_api'),
    path('api/register-api/',api_views.register_view,name='register_api'),
    path('api/logout-api/',api_views.logout_view,name='logout-api')
]
