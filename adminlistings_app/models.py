
from django.db import models

CURRENCIES = [('USD', "USD"),
              ('EUR', "EUR"),
              ('GBP', "GBP"),
              ('CAD', "CAD")]


class AdminListings(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=4)
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    image = models.ImageField(upload_to='product_images/', null=True)
    guidename = models.CharField(max_length=100)
    #upload = models.ImageField(upload_to='uploads/% Y/% m/% d/')

    def __str__(self):
        return f"{self.id}: {self.name} {self.description} costs {self.price} by {self.currency} (Guide: {self.guidename})"

    class Meta:
        ordering = ['-price']
from django.db import models