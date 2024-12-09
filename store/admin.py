from django.contrib import admin
from .models import Category, Prodotto, Marca

class Category_admin(admin.ModelAdmin):
    list_display = ('id', Category.__str__)

class Prodotto_admin(admin.ModelAdmin):
    list_display = ('id', Prodotto.__str__)

class Marca_admin(admin.ModelAdmin):
    list_display = ('id', Marca.__str__)
# Register your models here.
admin.site.register(Category, Category_admin)
admin.site.register(Prodotto, Prodotto_admin)
admin.site.register(Marca, Marca_admin)
