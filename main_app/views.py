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
