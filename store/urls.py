from django.urls import path
from .views import product_view, home_store, search

app_name = 'store'

urlpatterns = [
    path("", home_store, name='home_store'),
    path("product/<int:pk>/", product_view, name='product'),
    path("search/", search, name='search'),
]
