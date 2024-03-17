from django.contrib import admin

from .models import User, Offering, Rating, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Offering)
admin.site.register(Rating)
admin.site.register(Comment)