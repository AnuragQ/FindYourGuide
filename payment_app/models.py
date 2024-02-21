from django.db import models

from product_app.models import CURRENCIES, Product


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='USD')
    paid_at = models.DateTimeField(auto_now_add=True)
    payer = models.IntegerField(default=0)  # TODO Can be a foreign key
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    session_id = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return f"{self.amount} {self.currency} paid on  {self.paid_at} by {self.payer}"
