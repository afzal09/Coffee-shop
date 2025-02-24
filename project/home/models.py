from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .constants import PaymentStatus

class Coffee(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField(null=True)
    stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/',null=True)
    
    def __str__(self):
        return f"Coffee object - {self.name}"

class Orders(models.Model):
    orders_id = models.BigAutoField(primary_key=True)
    order_number = models.IntegerField()
    order_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=30)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    ordered_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    def __str__(self):
        return f"Order {self.name}, by {self.ordered_by.username}"
        pass

class Payments(models.Model):
    customer = models.CharField(max_length=255,null=True)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = models.CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def payment_status(self):
        return f"{self.id}-{self.name}-{self.status}"