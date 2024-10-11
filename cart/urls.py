from django.urls import path
from .views import cart_page, cart_add, cart_delete, cart_update

app_name = 'cart'

urlpatterns = [
    path("", cart_page, name="cart_page"),
    path("add/", cart_add, name="cart_add"),
    path("delete/", cart_delete, name="cart_delete"),
    path("update/", cart_update, name="cart_update"),

]