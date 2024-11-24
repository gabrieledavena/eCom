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
    is_sold=models.BooleanField(default=False)

    SIZE_CHOICES = [(i, str(i)) for i in range(37, 46)]
    size = models.IntegerField(choices=SIZE_CHOICES, default=37)
    likes = models.ManyToManyField(Customer, related_name='liked', blank=True)

    def __str__(self):
        return self.nome

