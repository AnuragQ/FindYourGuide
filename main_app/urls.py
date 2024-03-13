from django.urls import path
from django.contrib import admin
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('offerings/<int:pk>/', views.offering_detail, name='offering_detail'),
    path('payment/', include('payment_app.urls', namespace='payment_app')),
]