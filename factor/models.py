from django.db import models
from django.contrib.auth.models import User


class Factor(models.Model):
    FactorId = models.AutoField(primary_key=True)
    Description = models.TextField(blank=True)
    UserAddress = models.TextField()
    UserId = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    ShipmentStatus = models.BooleanField(default=False)
    ShipPrice = models.DecimalField(max_digits=6, decimal_places=2)
    OrderDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def total_price(self):
        total = self.ShipPrice
        for order in self.orders.all():
            total += order.Price
        return total

    def __str__(self):
        return f'{self.FactorId}{self.Description}{self.UserAddress}' \
               f'{self.UserId}{self.ShipmentStatus}{self.ShipPrice}{self.OrderDate}'

