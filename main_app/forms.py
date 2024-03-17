from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main_app.models import Offering


class CustomSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class OfferingForm(forms.ModelForm):
    class Meta:
        model = Offering
        fields = ['title', 'description', 'price', 'host_user', 'offering_type', 'offering_date', 'offering_time',
                  'offering_type']
