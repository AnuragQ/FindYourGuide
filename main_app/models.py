from datetime import datetime

from django.contrib.sessions.models import Session
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError
from django.utils import timezone


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
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    host_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='offerings', default=None)
    availability_start_date = models.DateField(default=None)
    availability_end_date = models.DateField(default=None)
    # type of enum
    OFFERING_TYPE_CHOICES = [
        ('accomodation', 'Accomodation'),
        ('sight-seeing', 'Sight-seeing'),
        ('food-tour', 'Food-tour'),
    ]
    offering_type = models.CharField(max_length=20, choices=OFFERING_TYPE_CHOICES, default='accomodation')
    offering_image = models.ImageField(null=True, default="Chevrolet-Equinox-40-of-45.jpg")
    offering_time = models.TimeField(null=True, blank=True)

    def clean(self):
        if self.availability_start_date > self.availability_end_date:
            raise ValidationError("Availability end date cannot be before availability start date")

    def save(self):
        self.full_clean()
        super().save()


class Rating(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=['offering', 'user'], name="unique_rating")]


class Comment(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    # let's allow rating without comments
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['offering', 'user'], name="unique_review_for_offering_user")
        ]


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

    def __str__(self):
        return f'Booking ID: {self.id}, Status: {self.booking_status}, guest: {self.guest_user.username}'


class LoginSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_sessions')
    session_key = models.CharField(max_length=50, blank=True)
    ip_address = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    browser_info = models.CharField(max_length=255)
    logged_at = models.DateTimeField(null=False)
    logged_out_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.session_key}, {self.user.username} {self.ip_address}, {self.location} {self.logged_at}'

    def save(self, *args, **kwargs):
        if not self.pk:  # This will check if it is a new object
            self.logged_at = datetime.now()
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if not self.pk:  # This will check if it is a new object
    #         self.logged_at = datetime.now()
    #     super().save(*args, **kwargs)


class Feedback(models.Model):
    title = models.CharField(max_length=50)
    feedback = models.TextField()
    ip_address = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    browser_info = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='feedbacks', null=True)
    def __str__(self):
        return f"{self.title}, {self.feedback}, {self.ip_address} {self.created_at}"
