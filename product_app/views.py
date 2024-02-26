import stripe
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http.response import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import View
from payment_app.models import Product, Payment
from django.conf import settings
from .models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductListView(ListView):
    model = Product
    template_name = 'product_app/products.html'


class ProductView(TemplateView):
    template_name = 'product_app\\product.html'

    def get_context_data(self, product_id, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get product information (you can adjust the logic to get the specific product you want)
        # product_id = self.request.GET.get('product_id')  # Assuming product_id is passed in the query parameters
        product = Product.objects.get(pk=product_id)

        # Add product information to the context
        context['product'] = product

        return context


class ProductAPI(View):

    def get(self, request):
        print("Getting products")
        products = Product.objects.all()
        data = {
            'data': list(products.values())  # Convert queryset to a list of dictionaries
        }
        return JsonResponse(data)


@csrf_exempt
def product_list_json(request):
    products = Product.objects.all()
    data = [{
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'currency': product.currency,
        'action': 'Proceed to Payment',
        'id': product.id,
        'image': product.image.url
    } for product in products]
    return JsonResponse({'data': data})
