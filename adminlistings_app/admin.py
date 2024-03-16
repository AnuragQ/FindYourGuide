from django.contrib import admin

from .models import AdminListings

# Register your models here.

# TODO only allow this under development
admin.site.register(AdminListings)