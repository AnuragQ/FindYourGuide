from django.shortcuts import render, get_object_or_404, redirect
from .models import Offering, User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomSignUpForm
from django.contrib.auth import logout
from .models import Offering, Booking
from django.db.models import Q



def index(request):
    q = request.GET.get(
        'search_query') if request.GET.get('search_query') != None else ''

    offerings = Offering.objects.filter(
        Q(title__icontains=q) | Q(description__icontains=q)
        # | Q(    host_user__username__icontains=q)
    )
    # print(offerings)
    context = {
        'offerings': offerings
    }
    return render(request, 'main_app/homepage.html', context)


def offering_detail(request, pk):
    offering = get_object_or_404(Offering, pk=pk)
    return render(request, 'main_app/offering_detail.html', {'offering': offering})


class SignUpView(CreateView):
    form_class = CustomSignUpForm
    # Redirect to homepage upon successful signup
    success_url = reverse_lazy('index')
    # Path to the template for sign up form
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # Save the user and return the super class's form_valid method
        response = super().form_valid(form)
        # Additional actions after successful form submission, if any
        return response


def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the homepage after logout

#def profile(request):
 #   return render(request, 'main_app/profile.html')

def profile(request):
    # Retrieve the services offered and services taken for the current user
    services_offered = Offering.objects.filter(host_user=request.user)
    services_taken = Booking.objects.filter(guest_user=request.user)

    # Pass the data to the template context
    context = {
        'services_offered': services_offered,
        'services_taken': services_taken,
    }

    return render(request, 'main_app/profile.html', context)


def editprofile(request):
    return render(request, 'main_app/editprofile.html')


