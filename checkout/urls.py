from django.urls import path
from .views import *
app_name = 'checkout'

urlpatterns = [
    path("", checkout, name="checkout"),

    path("accept_order/<int:order_id>", accept_order, name="accept_order"),


    path("notification/", notification_list, name="notification_list"),
    path("mark_as_read/<int:notification_id>", mark_as_read, name="mark_as_read"),

]