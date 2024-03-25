from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from user_agents import parse

from core.views import _get_location_from_ip
from .models import Offering, User, LoginSession
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomSignUpForm, OfferingForm, EditProfileForm, FeedbackForm
from django.contrib.auth import logout
from .models import Offering, Booking
from django.db.models import Q, Avg
from .models import Booking
from .forms import BookingForm

from .forms import RatingForm, ReviewOrderingForm, ReviewForm
from .models import Rating, Review

from .forms import RatingForm, ReviewOrderingForm, ReviewForm
from .models import Rating, Review

from django.contrib import messages


def index(request):
    q = request.GET.get(
        'search_query') if request.GET.get('search_query') != None else ''
    requesting_user = request.user
    if not requesting_user.is_authenticated:
       requesting_user=None
    offerings = Offering.objects.filter(
        Q(title__icontains=q) | Q(description__icontains=q)
        # | Q(    host_user__username__icontains=q)
    ).filter(is_available=True).exclude(host_user=requesting_user)

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

    return response


@login_required
def offering_edit(request, pk):
    offering = get_object_or_404(Offering, pk=pk)
    # Check if the current user is the host user of the offering
    print("request.method", request.method)

    if request.user == offering.host_user:
        if request.method == 'POST':
            form = OfferingForm(request.POST, request.FILES, instance=offering)
            if form.is_valid():
                form.host_user = request.user
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
            confirm = request.POST.get('confirm', None)
            print("confirm", confirm)

            if confirm == 'yes':
                offering.delete()
                # return HttpResponseRedirect('/homepage/')  # Redirect after deletion

                print("offering deleted")
                return redirect('index')
            else:
                print("offering not deleted")

                # Redirect back to offering detail page
                return redirect('offering_detail', pk=pk)
        else:
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
            # set offering as unavailable
            offering.is_available = False
            offering.save()
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
        # set offering as available
        offering = Offering.objects.get(id=booking.offering.id)
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
        print(f"Creating payment session for booking {booking.id}, {
              payment_session_duration_in_seconds} seconds")
        expiry_time = datetime.now() + timedelta(seconds=payment_session_duration_in_seconds)
        # or should it be an object with user id
        request.session['payment_expiry'] = expiry_time.timestamp()

    pending_with_price = True if booking.booking_status == 'pending' and booking.offering.price > 0 else False

    return render(request, 'main_app/booking_detail.html', {'booking': booking, 'offering': offering,
                                                            'pending_with_price': pending_with_price})


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
        form = OfferingForm(request.POST, request.FILES)
        print('=================')
        print(request.user)
        print('=================')
        # set host user to the current user
        form.host_user = request.user
        if form.is_valid():
            # Process the form data if valid
            # Get the offering instance without saving to database yet
            offering = form.save(commit=False)
            offering.host_user = request.user  # Set the host user
            offering.save()
            print('hello homepage inside save----')
            # Redirect to a success page or homepage
            # return render(request, 'main_app/homepage.html'+
            # )
            return redirect('index')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = OfferingForm()
        print('hello before final return')

    return render(request, 'main_app/addoffering.html', {'form': form})


def offering_page(req, pk):
    offering = get_object_or_404(Offering, pk=pk)
    reviews = offering.reviews.all()
    ratings = offering.ratings.all()
    comments = offering.comments.all()

    # Average Rating

    avg_rating_result = reviews.aggregate(avg_rating=Avg('score'))
    if avg_rating_result['avg_rating'] == None:
        avg_rating = 0
    else:
        avg_rating = round(avg_rating_result['avg_rating'])

    # avg_rating_result=ratings.aggregate(avg_rating=Avg('score'))
    # avg_rating=round(avg_rating_result['avg_rating'])

    # Total Comments
    total_comments = reviews.count()

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
            review, created = Review.objects.get_or_create(
                user=req.user,
                offering=offering,
                defaults={'score': form.cleaned_data['score'],
                          'text': form.cleaned_data['text']}
            )
            if not created:
                review.score = form.cleaned_data['score']
                review.text = form.cleaned_data['text']
                review.save()
            return redirect('offering_page', pk)

    if req.method == 'GET':
        form = ReviewForm()
    context = {'offering': offering,
               'reviews': reviews,
               'form': form,
               'avg_rating': avg_rating,
               'total_comments': total_comments,
               'review_order_form': review_order_form}
    response = render(req, 'main_app/offering_page.html', context)
    # Check if the offering id is in the cookie
    if 'recently_viewed_offerings' in req.COOKIES:

        recently_viewed_offerings = req.COOKIES['recently_viewed_offerings']
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


def user_profile(request, username):
    # Fetch the user object based on the username
    user = get_object_or_404(User, username=username)
    services_offered = Offering.objects.filter(host_user=user)
    # Render the user profile template with the user object
    return render(request, 'main_app/user_profile.html', {'profile_user': user, 'services_offered': services_offered})


@login_required
def get_login_sessions(request):
    login_sessions = LoginSession.objects.filter(user=request.user)
    return render(request, 'main_app/sessions.html', {'login_sessions': login_sessions})


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)

            print("Getting client info")
            ip_address = request.META.get('REMOTE_ADDR')
            user_agent = parse(request.META.get('HTTP_USER_AGENT'))
            location = _get_location_from_ip(ip_address)
            browser_info = user_agent.ua_string  # user_agent.browser.family
            feedback.ip_address = ip_address
            feedback.browser_info = browser_info
            feedback.location = location
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('/')  # Redirect to a thank you page
    else:
        form = FeedbackForm()

    return render(request, 'main_app/feedback.html', {'form': form})
