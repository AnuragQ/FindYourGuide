from django.shortcuts import render,get_object_or_404
from .models import Offering
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def index(request):
    return render(request, 'main_app/index.html')

def offering_detail(request, pk):
    offering = get_object_or_404(Offering, pk=pk)
    return render(request, 'main_app/offering_detail.html', {'offering': offering})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'main_app/signup.html', {'form': form})