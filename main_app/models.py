from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.
#


class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, unique=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    REQUIRED_FIELDS = []
    location = models.CharField(max_length=100, null=True)
    occupation = models.CharField(max_length=100, null=True)
    hobbies = models.TextField(null=True)
    languages = models.TextField(null=True)
    travel_destinations = models.TextField(null=True)
    goals = models.TextField(null=True)

class Offering(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    host_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='offerings', default=None)
    availability_start_date = models.DateField(default=None)
    availability_end_date = models.DateField(default=None)
    #type of enum
    OFFERING_TYPE_CHOICES = [
        ('accomodation', 'Accomodation'),
        ('sight-seeing', 'Sight-seeing'),
        ('food-tour', 'Food-tour'),
    ]
    offering_type = models.CharField(max_length=20, choices=OFFERING_TYPE_CHOICES,default='accomodation')
    offering_image = models.ImageField(null=True, default="Chevrolet-Equinox-40-of-45.jpg")
    offering_time = models.TimeField(null=True, blank=True)

class Rating(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

class Comment(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name='bookings')
    guest_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # host_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    booking_start_date = models.DateField(default=None)
    booking_end_date = models.DateField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    no_of_guests = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_status = models.CharField(
        max_length=20, choices=STATUS, default='pending')
