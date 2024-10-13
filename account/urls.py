import profile

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register, name= 'register'),
    path("Customerprofile/<int:pk>", CustomerProfileView.as_view(), name= 'customerprofile'),
    path("update_user/<int:pk>", CustomerUpdateView.as_view(), name= 'update_user'),
]
