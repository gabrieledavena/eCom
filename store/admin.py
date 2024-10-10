from django.contrib import admin
from .models import Category, Customer, Prodotto, Order
# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Prodotto)
admin.site.register(Order)