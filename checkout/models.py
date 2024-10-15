from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Notification(models.Model):
    recipient =models.ForeignKey(User,on_delete=models.CASCADE, related_name='notifications')
    message=models.TextField()
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notifica per {self.recipient.username}"
