from django.contrib import admin
from .models import Category, Prodotto, Marca

class Category_admin(admin.ModelAdmin):
    list_display = ('id', Category.__str__)
# Register your models here.
admin.site.register(Category, Category_admin)
admin.site.register(Prodotto)
admin.site.register(Marca)
