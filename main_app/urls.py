from django.urls import path
from django.contrib import admin
from django.urls import include
from . import views
from .views import SignUpView
from django.contrib.auth import views as auth_views

# app_name = 'main_app'  # Define the namespace here

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    # path('offering_detail/', views.offering_detail, name='offering_detail'),

    path('offerings/<int:pk>/', views.offering_detail, name='offering_detail'),
    path('payment/', include('payment_app.urls', namespace='payment_app')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', success_url='/'), name='login'),  # URL pattern for login
    path('logout/', views.logout_view, name='logout'),  # URL pattern for logout
 ]