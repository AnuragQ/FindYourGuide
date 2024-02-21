from unittest import skip

from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from unittest.mock import patch, MagicMock

from payment_app.models import Payment, Product


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_payments_view(self):
        response = self.client.get(reverse('payments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment_app/payments.html')

    #def test_success_view(self):
    #Hard to write


    def test_cancelled_view(self):
        response = self.client.get(reverse('cancelled'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment_app\\cancelled.html')

    def test_stripe_config(self):
        response = self.client.get(reverse('stripe_config'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_create_checkout_session(self):
        product = Product.objects.create(name='Test Product', description='Test Description', price=20, currency='USD')
        response = self.client.get('/payment/create-checkout-session/?product_id={}&quantity=1'.format(product.id))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    @skip("Skipping this test for now")
    def test_create_checkout_session_post(self):
        product = Product.objects.create(name='Test Product', description='Test Description', price=20, currency='USD')
        data = [{'product_id': product.id, 'quantity': 1}]
        response = self.client.post('/payment/create-checkout-session-post/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
