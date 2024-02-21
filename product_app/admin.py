from django.contrib import admin

from .models import Product

# Register your models here.

# TODO only allow this under development
admin.site.register(Product)