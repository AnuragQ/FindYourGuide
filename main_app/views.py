from django.shortcuts import render, get_object_or_404, redirect
from .models import Offering , Like,Comment
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomSignUpForm ,OfferingForm ,CommentForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'main_app/index.html')

from django.contrib.auth.decorators import login_required

def offering(req,pk):
    offering = get_object_or_404(Offering, pk=pk)
    comments = offering.comments.all()
    return render(req,'main_app/offer_detail.html',{'offering':offering, 'comments':comments})


def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = Like.objects.get_or_create(user=request.user, comment=comment)

    if not created:
        # Like already exists, so you might want to unlike it or do nothing
        like.delete()
    return redirect('offerings', pk=comment.offering.pk)

@login_required
def offering_detail(request, pk):
    offering = get_object_or_404(Offering, pk=pk)
    comments = offering.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.offering = offering
            comment.user = request.user
            comment.save()
            return redirect('offering_detail', pk=offering.pk)

    else:
        comment_form = CommentForm()

    context = {
        'offering': offering,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'main_app/offering_detail.html', context)


def offering_list(request):
    list_of_offerings = Offering.objects.all()
    if request.method == 'POST':
        form = OfferingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            price_min = form.cleaned_data.get('price_min')
            price_max = form.cleaned_data.get('price_max')
            host_user = form.cleaned_data.get('host_user')
            availability_start_date_min = form.cleaned_data.get('availability_start_date_min')
            availability_start_date_max = form.cleaned_data.get('availability_start_date_max')
            offering_type = form.cleaned_data['offering_type']

            # if No option is selected then it will return None
            if title:
                list_of_offerings = list_of_offerings.filter(title__icontains=title)
            if description:
                list_of_offerings = list_of_offerings.filter(description__icontains=description)
            if price_min:
                list_of_offerings = list_of_offerings.filter(price__gte=price_min)
            if price_max:
                list_of_offerings = list_of_offerings.filter(price__lte=price_max)
            if host_user:
                list_of_offerings = list_of_offerings.filter(host_user=host_user)
            if availability_start_date_min:
                list_of_offerings = list_of_offerings.filter(availability_start_date__gte=availability_start_date_min)
            if availability_start_date_max:
                list_of_offerings = list_of_offerings.filter(availability_start_date__lte=availability_start_date_max)
            if offering_type:
                list_of_offerings = list_of_offerings.filter(offering_type=offering_type)
    else:
        form = OfferingForm()
    return render(request,'main_app/offerings.html',{'list_of_offerings':list_of_offerings,'form':form})

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