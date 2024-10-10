from django.contrib import admin
from .models import Category, Prodotto, Order
# Register your models here.
admin.site.register(Category)
admin.site.register(Prodotto)
admin.site.register(Order)