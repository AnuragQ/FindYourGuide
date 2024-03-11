from django.contrib import admin

from .models import UserProfile, Offering, Rating, Comment

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Offering)
admin.site.register(Rating)
admin.site.register(Comment)