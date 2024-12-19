from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

class Coffee(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()
    quantity = models.IntegerField()
    stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/',null=True)
    
    def __str__(self):
        return f"Coffee object - {self.name}"

class Orders(models.Model):
    order_number = models.IntegerField()
    order_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=30)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    ordered_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    def __str__(self):
        return f"Order {self.name}, by {self.ordered_by.username}"
        pass

class Payment(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=[
        ('SUCCESS', 'Success'),
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"