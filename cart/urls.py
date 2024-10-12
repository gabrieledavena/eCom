from django.urls import path
from .views import cart_page, cart_add, cart_delete

app_name = 'cart'

urlpatterns = [
    path("", cart_page, name="cart_page"),
    path("add/", cart_add, name="cart_add"),
    path("delete/", cart_delete, name="cart_delete"),

]