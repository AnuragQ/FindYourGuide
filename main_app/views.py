from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Offering, User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomSignUpForm, OfferingForm
from django.contrib.auth import logout
from .models import Offering, Booking
from django.db.models import Q, Avg
from .models import Booking
from .forms import BookingForm

from .forms import RatingForm , ReviewOrderingForm ,ReviewForm
from .models import Rating, Review



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
    # Fetch all fields of the offering
    offering_fields = offering._meta.get_fields()
    # user_bookings containds the ids of the bookings made by the current user
    user_bookings = []
    # print('here')
    if request.user.is_authenticated:
        for booking in Booking.objects.filter(
                guest_user=request.user):
            user_bookings.append(booking.offering.id)
    # print(user_bookings)
    form = OfferingForm(instance=offering)  # Instantiate the form with the offering object
    return render(request, 'main_app/offering_detail.html', {'offering': offering, 'user_bookings': user_bookings,
                                                             'offering_fields': offering_fields, 'form': form})


# def offering_detail(request, pk):
#     offering = get_object_or_404(Offering, pk=pk)
#     user_bookings = []
#
#     # Check if the user is authenticated
#     if request.user.is_authenticated:
#         # Check if the current user is the host of the offering
#         if offering.host_user == request.user:
#             # Fetch all fields of the offering
#             offering_fields = offering._meta.get_fields()
#             # Populate user_bookings with the ids of bookings made by the current user
#             for booking in Booking.objects.filter(guest_user=request.user):
#                 user_bookings.append(booking.offering.id)
#             # Instantiate the form with the offering object
#             form = OfferingForm(instance=offering)
#             # Check if the request is POST (form submission)
#             if request.method == 'POST':
#                 # Check if the form data is valid
#                 form = OfferingForm(request.POST, request.FILES, instance=offering)
#                 if form.is_valid():
#                     form.save()
#                     # messages.success(request, 'Offering updated successfully.')
#                     return redirect('offering_detail', pk=pk)
#             return render(request, 'main_app/offering_detail.html', {'form': form})
#         else:
#             # If the current user is not the host, display a message and redirect
#             # messages.error(request, 'You are not authorized to edit this offering.')
#             return redirect('offering_detail', pk=pk)
#     else:
#         # If the user is not authenticated, redirect to login page
#         # messages.error(request, 'Please log in to edit this offering.')
#         return redirect('login')

@login_required
def offering_edit(request, pk):
    offering = get_object_or_404(Offering, pk=pk)
    # Check if the current user is the host user of the offering
    if request.user == offering.host_user:
        if request.method == 'POST':
            form = OfferingForm(request.POST, request.FILES, instance=offering)
            if form.is_valid():
                form.save()
                return redirect('offering_detail', pk=pk)
        else:
            form = OfferingForm(instance=offering)
        return render(request, 'main_app/editoffering.html', {'form': form})
    else:
        return redirect('offering_detail', pk=pk)  # Redirect if the user is not the host


@login_required
def offering_delete(request, pk):
    offering = get_object_or_404(Offering, pk=pk)
    # Check if the current user is the host user of the offering
    if request.user == offering.host_user:
        if request.method == 'POST':
            offering.delete()
            return redirect('homepage')  # Redirect after deletion
        return render(request, 'main_app/deleteoffering.html', {'offering': offering})
    else:
        return redirect('offering_detail', pk=pk)  # Redirect if the user is not the host


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


def create_booking(request, offering_id):
    form = BookingForm()
    # if request.method == 'POST':
    offering = Offering.objects.get(id=offering_id)
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.offering = offering
            booking.guest_user = request.user
            booking.save()
            return redirect('index')
    context = {'form': form}

    # return redirect('index')
    return render(request, 'main_app/booking.html', context)


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    print(booking)
    # Ensure that only the user who made the booking can cancel it
    if request.user == booking.guest_user:
        booking.delete()
        # Redirect to a booking list page or any other page
        return redirect('index')
    else:
        # Handle unauthorized cancel attempt (optional)
        return render(request, 'error.html', {'message': 'You are not authorized to cancel this booking.'})


def profile(request):
    return render(request, 'main_app/profile.html')


def editprofile(request):
    return render(request, 'main_app/editprofile.html')


def addoffering(request):
    if request.method == 'POST':
        form = OfferingForm(request.POST)
        if form.is_valid():
            # Process the form data if valid
            form.save()
            print('hello homepage inside save')
            # Redirect to a success page or homepage
            return render(request, 'main_app/addoffering.html')
    else:
        form = OfferingForm()
    return render(request, 'main_app/addoffering.html', {'form': form})

def offering_page(req,pk):

    offering = get_object_or_404(Offering, pk=pk)
    reviews = offering.reviews.all()
    ratings =offering.ratings.all()
    comments = offering.comments.all()

    # Average Rating

    avg_rating_result = reviews.aggregate(avg_rating=Avg('score'))
    if avg_rating_result['avg_rating'] == None:
        avg_rating=0
    else:
        avg_rating = round(avg_rating_result['avg_rating'])






    # avg_rating_result=ratings.aggregate(avg_rating=Avg('score'))
    # avg_rating=round(avg_rating_result['avg_rating'])

    #Total Comments
    total_comments=reviews.count()

    # total_comments= comments.count()

    # Handle comment ordering form
    review_order_form = ReviewOrderingForm(req.GET)
    if review_order_form.is_valid():
        order_by = review_order_form.cleaned_data.get('order_by')
        if order_by == 'latest':
            reviews = reviews.order_by('-created_at')
        elif order_by == 'oldest':
            reviews = reviews.order_by('created_at')
        elif order_by == 'highest_rating':
            reviews = reviews.order_by('-score')
        elif order_by == 'lowest_rating':
            reviews = reviews.order_by('score')


    if req.method == 'POST':
        # if user has already rated
        form = ReviewForm(req.POST)
        if form.is_valid():
            # here user and offering attributes are used to get object if there is object
            # default value attibutes like score are used to assign values to those attributes if cannot get that object
            # Also get_or_created is not used to do any update
            review,created=Review.objects.get_or_create(
                user=req.user,
                offering=offering,
                defaults={'score': form.cleaned_data['score'],
                          'text': form.cleaned_data['text']}
            )
            if not created:
                review.score=form.cleaned_data['score']
                review.text = form.cleaned_data['text']
                review.save()
            return redirect('offering_page', pk)

    if req.method == 'GET':
        form = ReviewForm()
    context ={'offering': offering,
              'ratings': ratings,
              'reviews': reviews,
              'form': form,
              'avg_rating': avg_rating,
              'comments': comments,
              'total_comments': total_comments,
              'review_order_form': review_order_form }
    return render(req,'main_app/offering_page.html',context)





