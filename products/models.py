from django.db import models


class Products(models.Model):
    ProductId = models.AutoField(primary_key=True, blank=False)
    ProductName = models.CharField(max_length=20)
    ProductImage = models.ImageField(null=True, blank=True)
    ProductQuantity = models.IntegerField()
    ProductPrice = models.DecimalField(max_digits=6, decimal_places=2)
    ProductDescription = models.TextField()
