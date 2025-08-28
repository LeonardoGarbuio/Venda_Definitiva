from django.urls import path
from . import views

app_name = 'motoboys'

urlpatterns = [
    path('login/', views.motoboy_login, name='login'),
    path('logout/', views.motoboy_logout, name='logout'),
    path('check-status/', views.check_motoboy_status, name='check_status'),
    path('check-device/', views.check_device_status, name='check_device'),
    path('register/', views.motoboy_register, name='register'),
    path('dashboard/', views.motoboy_dashboard, name='dashboard'),
    path('profile/', views.motoboy_profile, name='profile'),
    path('orders/', views.motoboy_orders, name='orders'),
    path('update-location/', views.update_motoboy_location, name='update_location'),
    path('update-status/', views.update_motoboy_status, name='update_status'),
    path('accept-order/', views.accept_order, name='accept_order'),
    path('update-order-status/', views.update_order_status, name='update_order_status'),
]
