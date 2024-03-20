from django.contrib import admin

from .models import User, Offering, Rating, Comment, Booking

# Register your models here.
admin.site.register(User)
admin.site.register(Offering)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Booking)