from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'store'

urlpatterns = [
    path("", home_store, name='home_store'),
    path("product/<int:pk>/", product_view, name='product'),
]
