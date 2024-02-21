from django.urls import path

from . import views

urlpatterns = [
    path('', views.payments_view, name='payments'),
    path('products/<int:product_id>', views.PaymentView.as_view(), name='payment'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.success_view),
    path('cancelled/', views.CancelledView.as_view())
]