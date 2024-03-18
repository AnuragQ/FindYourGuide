from django.urls import path
from django.contrib import admin
from django.urls import include
from . import views
from .views import SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    # path('offering_detail/', views.offering_detail, name='offering_detail'),
    path('offerings/<int:pk>/edit/', views.offering_edit, name='offering_edit'),
    path('offerings/<int:pk>/delete/', views.offering_delete, name='offering_delete'),
    path('offerings/<int:pk>/', views.offering_detail, name='offering_detail'),
    path('payment/', include('payment_app.urls', namespace='payment_app')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',
         success_url='/'), name='login'),  # URL pattern for login
    path('logout/', views.logout_view, name='logout'),  # URL pattern for logout
    path('create_booking/<int:offering_id>',
         views.create_booking, name='create_booking'),
    path('cancel_booking/<int:booking_id>', views.cancel_booking, name='cancel_booking'),
    # path('bookings/<int:pk>/', views.offering_detail, name='offering_detail'),

    path('profile', views.profile, name='profile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('addoffering/', views.addoffering, name='addoffering'),
]