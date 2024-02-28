from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views  # Import Django's authentication views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('offerings/<int:pk>/', views.offering_detail, name='offering_detail'),

    # Add paths for authentication
    path('login/', auth_views.LoginView.as_view(template_name='main_app/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),  # Replace 'signup' with your actual signup view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
