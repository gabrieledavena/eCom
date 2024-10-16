from django.urls import path
from .views import *

app_name = 'checkout'

urlpatterns = [
    path("", checkout, name="checkout"),

    path("supplierorderview", SupplierOrderView.as_view(), name="supplierorderview"),
    path("accept_order/<int:order_id>", accept_order, name="accept_order"),
    path("reject_order/<int:order_id>", reject_order, name="reject_order"),


    path("notification/", notification_list, name="notification_list"),
    path("mark_as_read/<int:notification_id>", mark_as_read, name="mark_as_read"),

]