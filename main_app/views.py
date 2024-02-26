from django.shortcuts import render,get_object_or_404
from .models import Offering
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

def index(request):
    return render(request, 'main_app/index.html')

def offering_detail(request, pk):
    offering = get_object_or_404(Offering, pk=pk)
    return render(request, 'main_app/offering_detail.html', {'offering': offering})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'main_app/signup.html'  # Create this template in your 'templates/main_app/' folder

class CustomLoginView(LoginView):
    template_name = 'main_app/login.html'  # Create this template in your 'templates/main_app/' folder

class CustomPasswordResetView(PasswordResetView):
    template_name = 'main_app/password_reset.html'  # Create this template in your 'templates/main_app/' folder