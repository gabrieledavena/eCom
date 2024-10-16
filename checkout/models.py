from django.contrib.auth.models import User
from django.db import models

from account.models import Customer, Supplier
from cart import cart
from store.models import Prodotto


# Create your models here.
class Notification(models.Model):
    recipient =models.ForeignKey(User,on_delete=models.CASCADE, related_name='notifications')
    message=models.TextField()
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notifica per {self.recipient.username}"

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE, related_name='orders')
    created_at=models.DateTimeField(auto_now_add=True)
    supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE, related_name='orders')

    class OrderStatus(models.TextChoices):
        PENDING='PENDING'
        ACCEPTED='ACCEPTED'
        REJECTED='REJECTED'
        COMPLETED='COMPLETED'

    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.PENDING, max_length=20)

    def __str__(self):
        return f"Order {self.id}, from {self.customer}"

    def get_total(self):
        return sum(item.prodotto.price  for item in self.items.all())

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name='items')
    prodotto = models.ForeignKey(Prodotto,on_delete=models.CASCADE)
