from django.contrib import admin
from .models import Supplier, Customer
# Register your models here.
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', Supplier.__str__)
    

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', Customer.__str__)
  
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Customer, CustomerAdmin)