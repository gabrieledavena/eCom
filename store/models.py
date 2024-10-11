from django.db import models
import datetime
from django.contrib.auth.models import User
from account.models import Supplier, Customer
# Create your models here.
class Category(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Prodotto(models.Model):
    nome= models.CharField( max_length=50)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default = 1)
    description =models.CharField( max_length=200, blank=True)
    image = models.ImageField(upload_to='uploads/product', blank=True, default='uploads/product/stock_shoes.jpg')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Order(models.Model):
    product=models.ForeignKey(Prodotto, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=50, default='', blank=True)
    phone=models.CharField(max_length=20, default='', blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.product