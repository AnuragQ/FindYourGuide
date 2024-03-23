import json

import stripe
from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from main_app.models import Booking
from payment_app.models import Product
from .models import Payment
from django.db.models import Q

stripe.api_key = settings.STRIPE_SECRET_KEY


def payments_view(request):
    payments = Payment.objects.filter(payer=request.user)
    # payments = Payment.objects.filter(Q(payer=request.user) | Q(booking__offering__host_user=request.user))
    return render(request, 'payment_app/payments.html', {'payments': payments})


def success_view(request):
    session_id = request.GET.get('session_id')
    booking_id = request.GET.get('booking_id')

    # Record the payment here if needed
    print("Getting session info")
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    booking = Booking.objects.get(id=booking_id)

    # payment = Payment.objects.get(session_id=session_id)
    payment = Payment.objects.filter(session_id=session_id).first()

    if payment is None:
        amount_total = checkout_session.amount_total / 100  # Decimal(str())
        payment = Payment.objects.create(
            amount=amount_total,
            currency=checkout_session.currency,
            payer=request.user,
            booking=booking,
            session_id=session_id
        )
        print(f"Payment {payment.id} created successfully")
        booking.booking_status = 'confirmed'
        booking.save()
        print(f"Booking {booking_id} updated successfully")
    else:
        print("Payment already exists")

    context = {"booking_id": booking_id, "offering_id": booking.offering_id}
    return render(request, 'payment_app/success.html', context)


class CancelledView(TemplateView):
    template_name = 'payment_app\\cancelled.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


# Not used
def get_stripe_payment_info(request, session_id):
    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        return JsonResponse(checkout_session)
    except stripe.error.InvalidRequestError:
        return JsonResponse({'error': 'Invalid Session ID'}, status=400)


# Not used
@csrf_exempt
def create_checkout_session_post(request):
    if request.method == 'POST':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            data = json.loads(request.body.decode('utf-8'))
            line_items = []
            for item in data:
                product_id = item.get('product_id')
                quantity = item.get('quantity')
                # Retrieve product details (e.g., name, price) from database based on product_id
                product = Product.objects.get(pk=product_id)
                line_item = {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price * 100,  # Convert price to cents
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': quantity,
                }
                line_items.append(line_item)

            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'payment/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'payment/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                currency='usd',
                line_items=line_items,
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            booking_id = request.GET.get('booking_id')

            # Retrieve product details (e.g., name, price) from the database based on the product_id
            booking = Booking.objects.get(pk=booking_id)

            # Construct line item for Stripe Checkout with the specified quantity
            line_item = {
                'quantity': 1,
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(booking.offering.price * 100),  # Convert price to cents
                    'product_data': {
                        'name': booking.offering.title,
                        'images': [domain_url + booking.offering.offering_image.url]
                    },
                },
            }

            # Create a checkout session with the constructed line item
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + f'payment/success?session_id={{CHECKOUT_SESSION_ID}}&booking_id={booking_id}',
                cancel_url=domain_url + 'payment/cancelled/',
                # success_url=request.build_absolute_uri(reverse('success_url')),
                # cancel_url=request.build_absolute_uri(reverse('cancel_url')),
                payment_method_types=['card'],
                mode='payment',
                currency='usd',
                line_items=[line_item]
            )

            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)
