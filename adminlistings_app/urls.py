from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.AdminListingsListView.as_view(), name='adminlistings'),
    path('<int:adminlistings_id>', views.AdminListingsView.as_view(), name='adminlistings'),
    path('api/adminlistings', views.adminlistings_list_json, name='adminlistings_api'),
    #path('api/adminlistings/test', views.AdminListingsAPI.as_view(), name='adminlistings_api'),
    path('api/adminlistings/', views.AdminListingsListView.as_view(), name='adminlistings_api'),  # Add this line

]