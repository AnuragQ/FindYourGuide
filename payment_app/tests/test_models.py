from django.test import TestCase
from django.utils import timezone
from payment_app.models import Payment
from product_app.models import Product


class PaymentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a Product instance for testing
        cls.product = Product.objects.create(name='Test Product', description='Test description', price=10.00,
                                             currency='USD')

    def test_payment_creation(self):
        # Create a Payment instance
        payment = Payment.objects.create(amount=20.00, currency='USD', payer=1, product=self.product)

        # Check if the Payment instance was created successfully
        self.assertTrue(isinstance(payment, Payment))
        self.assertEqual(payment.amount, 20.00)
        self.assertEqual(payment.currency, 'USD')
        self.assertEqual(payment.payer, 1)
        self.assertEqual(payment.product, self.product)

    def test_str_method(self):
        payment = Payment.objects.create(amount=20.00, currency='USD', payer=1, product=self.product)
        expected_str = f"{payment.amount} {payment.currency} paid on {payment.paid_at} by {payment.payer}"
        self.assertEqual(str(payment), expected_str)

    def test_session_id_nullable(self):
        payment = Payment.objects.create(amount=20.00, currency='USD', payer=1, product=self.product)
        self.assertIsNone(payment.session_id)
