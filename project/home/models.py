from django.db import models

class Coffee(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()
    quantity = models.IntegerField()
    stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/',null=True)
