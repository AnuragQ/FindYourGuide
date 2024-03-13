from django.shortcuts import render,get_object_or_404,redirect
from .models import Offering
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'main_app/index.html')

#def offering_detail(request, pk):
    #offering = get_object_or_404(Offering, pk=pk)
    #return render(request, 'main_app/offering_detail.html', {'offering': offering})


def offering_detail(request, pk):
    offering = get_object_or_404(Offering, pk=pk)
    comments = offering.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.offering = offering
            comment.user = request.user.userprofile
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
