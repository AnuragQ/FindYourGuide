from django import forms

from django.contrib.auth.forms import UserCreationForm ,UserChangeForm
from .models import User, Booking, Offering,Rating,Review

from django.forms import ModelForm


from main_app.models import Offering


class CustomSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')


class BookingForm(ModelForm):

    class Meta:
        model = Booking
        fields = ['booking_start_date', 'booking_end_date', 'no_of_guests']
        widgets = {
            'booking_start_date': forms.DateInput(attrs={'type': 'date', 'min': '2024-02-15', 'max': '2024-04-30'}),
            'booking_end_date': forms.DateInput(attrs={'type': 'date'})
        }


class OfferingForm(forms.ModelForm):
    class Meta:
        model = Offering
        fields = ['title', 'description', 'price', 'host_user', 'availability_start_date', 'availability_end_date',
                  'offering_type', 'offering_image', 'offering_time'
                  ]
        widgets = {
            'availability_start_date': forms.DateInput(attrs={'type': 'date'}),
            'availability_end_date': forms.DateInput(attrs={'type': 'date'})
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model=Rating
        fields = ['score']

class CommentOrderingForm(forms.Form):
    ORDER_CHOICES = (
        ('latest', 'Latest'),
        ('oldest', 'Oldest'),
        ('highest_rating', 'Highest Rating'),
        ('lowest_rating', 'Lowest Rating'),
    )
    order_by = forms.ChoiceField(choices=ORDER_CHOICES, label='Order By')

class ReviewForm(forms.ModelForm):
    SCORE_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    score = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.Select(), label='Rating')
    class Meta:
        model = Review
        fields = ['score', 'text']
        labels = { 'text': 'Comment'}

class ReviewOrderingForm(forms.Form):
    ORDER_CHOICES = (
        ('latest', 'Latest'),
        ('oldest', 'Oldest'),
        ('highest_rating', 'Highest Rating'),
        ('lowest_rating', 'Lowest Rating'),
    )
    order_by = forms.ChoiceField(choices=ORDER_CHOICES, label='Order By')
=======
class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'bio', 'location', 'occupation', 'hobbies', 'languages', 'travel_destinations', 'goals', 'avatar')

