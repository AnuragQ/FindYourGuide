from django.urls import path
from django.contrib import admin
from django.urls import include
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('offerings/<int:pk>/', views.offering_detail, name='offering_detail'),
    path('payment/', include('payment_app.urls', namespace='payment_app')),
    path('signup/', SignUpView.as_view(), name='signup'),
]