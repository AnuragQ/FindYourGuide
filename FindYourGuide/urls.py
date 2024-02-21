from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('payment/', include('payment_app.urls')),
    path('products/', include('product_app.urls')),
]
