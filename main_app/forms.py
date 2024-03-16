from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Offering,UserProfile,Comment

class CustomSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class OfferingForm(forms.Form):
    offering_type_choices = [(None, "-------")] +Offering.OFFERING_TYPE_CHOICES
    offering_type = forms.ChoiceField(choices=offering_type_choices,required=False,initial=None)
    # Other fields
    title = forms.CharField(max_length=200, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    price_min = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    price_max = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    host_user = forms.ModelChoiceField(queryset=UserProfile.objects.all(), required=False)
    availability_start_date_min = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}))
    availability_start_date_max = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date'}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add a Comment...', 'class': 'form-control', 'rows': 3}),
        }