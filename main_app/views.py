from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Offering, User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomSignUpForm, OfferingForm, EditProfileForm
from django.contrib.auth import logout
from .models import Offering, Booking
from django.db.models import Q, Avg
from .models import Booking
from .forms import BookingForm

from .forms import RatingForm , ReviewOrderingForm ,ReviewForm
from .models import Rating, Review


from .forms import RatingForm , ReviewOrderingForm ,ReviewForm
from .models import Rating, Review


from django.contrib import messages

def index(request):
    q = request.GET.get(
        'search_query') if request.GET.get('search_query') != None else ''

    offerings = Offering.objects.filter(
        Q(title__icontains=q) | Q(description__icontains=q)
        # | Q(    host_user__username__icontains=q)
    )
    recently_viewed_offerings = []
    if 'recently_viewed_offerings' in request.COOKIES:
        # Get the cookie value
        recently_viewed_offerings_ids = request.COOKIES['recently_viewed_offerings']
        # Split the cookie value into a list
        recently_viewed_offerings_ids = recently_viewed_offerings_ids.split(
            ',')
        # Fetch the offerings with the ids in the list
        recently_viewed_offerings = Offering.objects.filter(
            id__in=recently_viewed_offerings_ids)

    # print(offerings)
    context = {
        'offerings': offerings,
        'recently_viewed_offerings': recently_viewed_offerings
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

    # set the cookie value
    # Instantiate the form with the offering object
    form = OfferingForm(instance=offering)
    response = render(request, 'main_app/offering_detail.html', {'offering': offering, 'user_bookings': user_bookings,
                                                                 'offering_fields': offering_fields, 'form': form})
    # Check if the offering id is in the cookie
    if 'recently_viewed_offerings' in request.COOKIES:
        recently_viewed_offerings = request.COOKIES['recently_viewed_offerings']
        # Split the cookie value into a list
        recently_viewed_offerings = recently_viewed_offerings.split(',')
        # Check if the offering id is already in the list
        if str(pk) in recently_viewed_offerings:
            # Remove the offering id from the list
            recently_viewed_offerings.remove(str(pk))
        # Add the offering id to the beginning of the list
        recently_viewed_offerings.insert(0, str(pk))
        # Keep the list length to 5
        recently_viewed_offerings = recently_viewed_offerings[:5]
        # Join the list into a string
        recently_viewed_offerings = ','.join(recently_viewed_offerings)
    else:
        # If the cookie does not exist, set the cookie value to the offering id
        recently_viewed_offerings = str(pk)

    # Set the cookie value
    response.set_cookie('recently_viewed_offerings', recently_viewed_offerings)
    return response

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
        # Redirect if the user is not the host
        return redirect('offering_detail', pk=pk)


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
        # Redirect if the user is not the host
        return redirect('offering_detail', pk=pk)


# class SignUpView(CreateView):
#     form_class = CustomSignUpForm
#     # Redirect to homepage upon successful signup
#     success_url = reverse_lazy('index')
#     # Path to the template for sign up form
#     template_name = 'registration/signup.html'
#
#     def form_valid(self, form):
#         # Save the user and return the super class's form_valid method
#         response = super().form_valid(form)
#         # Additional actions after successful form submission, if any
#         return response
#
#
# def logout_view(request):
#     logout(request)
#     return redirect('index')  # Redirect to the homepage after logout


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
            booking.status = 'pending'
            booking.save()

            return redirect('booking_detail', pk=booking.id)
    context = {'form': form}

    # return redirect('index')
    return render(request, 'main_app/booking.html', context)


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    print(booking)
    # Ensure that only the user who made the booking can cancel it
    if request.user == booking.guest_user:
        # chenge the status of the booking to cancelled
        booking.booking_status = 'cancelled'
        booking.save()
        print("Removing payment expiry session")
        if 'payment_expiry' in request.session:
            del request.session['payment_expiry']
        # Redirect to a booking list page or any other page
        return redirect('index')
    else:
        # Handle unauthorized cancel attempt (optional)
        return render(request, 'error.html', {'message': 'You are not authorized to cancel this booking.'})


def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # if booking exists, fetch the offering
    offering = None
    if booking:
        offering = Offering.objects.get(id=booking.offering.id)


    if booking.booking_status == 'pending':
        payment_session_duration_in_seconds = 60
        print(f"Creating payment session for booking {booking.id}, {payment_session_duration_in_seconds} seconds")
        expiry_time = datetime.now() + timedelta(seconds=payment_session_duration_in_seconds)
        request.session['payment_expiry'] = expiry_time.timestamp()  # or should it be an object with user id

    return render(request, 'main_app/booking_detail.html', {'booking': booking, 'offering': offering})


# def profile(request):
#    return render(request, 'main_app/profile.html')


def profile(request):
    # Fetch data for services offered and services taken
    services_offered = Offering.objects.filter(host_user=request.user)
    services_taken = Booking.objects.filter(guest_user=request.user)

    context = {
        'services_offered': services_offered,
        'services_taken': services_taken
    }
    return render(request, 'main_app/profile.html', context)




def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Redirect to the profile page after successful edit
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'main_app/editprofile.html', {'form': form})


def addoffering(request):
    if request.method == 'POST':
        form = OfferingForm(request.POST)
        if form.is_valid():
            # Process the form data if valid
            form.save()
            print('hello homepage inside save')
            # Redirect to a success page or homepage
            return render(request, 'main_app/homepage.html')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
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
              'reviews': reviews,
              'form': form,
              'avg_rating': avg_rating,
              'total_comments': total_comments,
              'review_order_form': review_order_form }
    return render(req,'main_app/offering_page.html',context)




def user_profile(request, username):
    # Fetch the user object based on the username
    user = get_object_or_404(User, username=username)
    # Render the user profile template with the user object
    return render(request, 'main_app/user_profile.html', {'profile_user': user})

