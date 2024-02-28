from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('offerings/<int:pk>/', views.offering_detail, name='offering_detail'),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('signup/', views.signup, name='signup'),


]