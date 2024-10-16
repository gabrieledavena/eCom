from django.contrib import admin

from checkout.models import Notification, Order, OrderItem

# Register your models here.
admin.site.register(Notification)
admin.site.register(OrderItem)
admin.site.register(Order)