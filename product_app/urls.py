from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('<int:product_id>', views.ProductView.as_view(), name='product'),
    path('api/products', views.product_list_json, name='products_api'),
    #path('api/products/test', views.ProductAPI.as_view(), name='products_api'),
]