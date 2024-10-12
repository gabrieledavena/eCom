from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Supplier(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='supplier')
    is_supplier = models.BooleanField(default=False) 

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    nome= models.CharField(default='', max_length=50)
    cognome = models.CharField(default='', max_length=50)
    email =models.EmailField(default='', max_length=50)
    password= models.CharField(default='', max_length=50)
    indirizzo = models.CharField(default='', max_length=50)
    def __str__(self):
        return f'{self.user.username} {self.cognome} {self.nome}'