from django.db import models
from django.contrib.auth.models import User

class orders(models.Model):
    name = models.CharField(max_length=30)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    ordered_by = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
def __str__(self):
    return "%s the restaurant" % self.ordered_by.username
    pass


class Coffee(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()
    quantity = models.IntegerField()
    stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/',null=True)
