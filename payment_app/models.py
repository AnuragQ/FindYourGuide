from django.db import models

from main_app.models import Booking, User
from product_app.models import Product

CURRENCIES = [('USD', "USD"),
              ('EUR', "EUR"),
              ('GBP', "GBP"),
              ('CAD', "CAD")]


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='USD')
    paid_at = models.DateTimeField(auto_now_add=True)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='bookings', null=True)
    session_id = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return f"{self.amount} {self.currency} paid on {self.paid_at} by {self.payer}"
