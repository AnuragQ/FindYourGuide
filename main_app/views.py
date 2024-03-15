from django.shortcuts import render, get_object_or_404, redirect
from .models import Offering
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomSignUpForm
from django.contrib.auth import logout

def index(request):
    return render(request, 'main_app/index.html')

def offering_detail(request, pk):
    offering = get_object_or_404(Offering, pk=pk)
    return render(request, 'main_app/offering_detail.html', {'offering': offering})

class SignUpView(CreateView):
    form_class = CustomSignUpForm
    success_url = reverse_lazy('index')  # Redirect to homepage upon successful signup
    template_name = 'registration/signup.html'  # Path to the template for sign up form

    def form_valid(self, form):
        # Save the user and return the super class's form_valid method
        response = super().form_valid(form)
        # Additional actions after successful form submission, if any
        return response

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the homepage after logout