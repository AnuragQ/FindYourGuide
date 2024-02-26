from django.urls import path

from . import views

urlpatterns = [
    path('', views.payments_view, name='payments'),
    path('config/', views.stripe_config, name="stripe_config"),
    path('create-checkout-session/', views.create_checkout_session, name="create_checkout_session"),
    path('success/', views.success_view, name="success"),
    path('cancelled/', views.CancelledView.as_view(), name="cancelled")
]
