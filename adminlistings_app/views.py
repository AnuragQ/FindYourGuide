
import stripe
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic import View
from django.views.generic.base import TemplateView

from .models import AdminListings

stripe.api_key = settings.STRIPE_SECRET_KEY


class AdminListingsListView(ListView):
    model = AdminListings
    template_name = 'adminlistings_app/adminlistings.html'


class AdminListingsView(TemplateView):
    template_name = 'adminlistings_app\\adminlistings.html'

    def get_context_data(self, adminlistings_id, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get adminlistings information (you can adjust the logic to get the specific adminlistings you want)
        # adminlistings_id = self.request.GET.get('adminlistings_id')  # Assuming adminlistings_id is passed in the query parameters
        adminlistings = AdminListings.objects.get(pk=adminlistings_id)

        # Add adminlistings information to the context
        context['adminlistings'] = adminlistings

        return context


class AdminListingsAPI(View):

    def get(self, request):
        print("Getting adminlistings")
        adminlistings = AdminListings.objects.all()
        data = {
            'data': list(adminlistings.values())  # Convert queryset to a list of dictionaries
        }
        return JsonResponse(data)


@csrf_exempt
def adminlistings_list_json(request):
    adminlistings = AdminListings.objects.all()
    data = [{
        'name': adminlistings.name,
        'description': adminlistings.description,
        'price': adminlistings.price,
        'currency': adminlistings.currency,
        'action': 'Proceed to Payment',
        'id': adminlistings.id,
        'image': adminlistings.image.url,
        'guidename': adminlistings.guidename
    } for adminlistings in adminlistings]
    return JsonResponse({'data': data})