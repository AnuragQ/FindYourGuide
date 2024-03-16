from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.
#
class UserProfile(User):
    # USER_TYPE_CHOICES = [
    #     ('guest', 'Guest'),
    #     ('host', 'Host'),
    # ]
    # #email = models.EmailField(unique=True)
    # user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='guest')
    
    def __str__(self):
        return self.username

class Offering(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    host_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='offerings')
    availability_start_date = models.DateField()
    availability_end_date = models.DateField()
    #type of enum
    OFFERING_TYPE_CHOICES = [
        ('accomodation', 'Accomodation'),
        ('sight-seeing', 'Sight-seeing'),
        ('food-tour', 'Food-tour'),
        ('ride-share','Ride-Share')
    ]
    offering_type = models.CharField(max_length=20, choices=OFFERING_TYPE_CHOICES, default='accomodation')
class Rating(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

class Comment(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name='bookings')
    guest_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # host_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)