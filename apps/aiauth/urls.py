from django.urls import path
from . import views


app_name = 'aiauth'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('resetpwd', views.ResetPassword.as_view(), name='resetpwd'),
    path('users', views.UserManager.as_view(), name='users')
]