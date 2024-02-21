from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('api/products', views.product_list_json, name='products_api'),
    #path('api/products/test', views.ProductAPI.as_view(), name='products_api'),
    #path('products/<int:payment_id>', views.PaymentView.as_view(), name='payment'),
]