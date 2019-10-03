from django.db import models
from products.models import Products
from factor.models import Factor


class Order(models.Model):
    OrderId = models.AutoField(primary_key=True)
    ProductId = models.ForeignKey(Products, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Price = models.DecimalField(max_digits=6, decimal_places=2)
    FactorId = models.ForeignKey(Factor, null=True, related_name='orders', on_delete=models.CASCADE)