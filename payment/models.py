import datetime
from django.db import models
from factor.models import Factor


class Payment(models.Model):
    PaymentId = models.AutoField(primary_key=True)
    FactorId = models.ForeignKey(Factor, on_delete=models.CASCADE)
    PaymentStatus = models.BooleanField(default=False)
    PaymentAmount = models.DecimalField(max_digits=6, decimal_places=2)
    PaymentDate = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)

    def __str__(self):
        return f'{self.PaymentId}{self.FactorId}{self.PaymentStatus}' \
               f'{self.PaymentAmount}{self.PaymentDate}'
