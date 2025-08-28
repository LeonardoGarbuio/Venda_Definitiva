from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('profile/', views.user_profile, name='profile'),
    path('orders/', views.user_orders, name='orders'),
    path('orders/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('update-location/', views.update_user_location, name='update_location'),
]
