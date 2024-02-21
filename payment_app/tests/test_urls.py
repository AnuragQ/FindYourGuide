from django.test import SimpleTestCase
from django.urls import reverse, resolve
from payment_app.views import payments_view, success_view, CancelledView, stripe_config, create_checkout_session


class TestUrls(SimpleTestCase):

    def test_payments_url_resolves(self):
        url = reverse('payments')
        self.assertEqual(resolve(url).func, payments_view)

    def test_success_url_resolves(self):
        url = reverse('success')
        self.assertEqual(resolve(url).func, success_view)

    def test_cancelled_url_resolves(self):
        url = reverse('cancelled')
        self.assertEqual(resolve(url).func.view_class, CancelledView)

    def test_stripe_config_url_resolves(self):
        url = reverse('stripe_config')
        self.assertEqual(resolve(url).func, stripe_config)

    def test_create_checkout_session_url_resolves(self):
        url = reverse('create_checkout_session')
        self.assertEqual(resolve(url).func, create_checkout_session)
