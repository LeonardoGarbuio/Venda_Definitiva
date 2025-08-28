from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create'),
    path('list/', views.order_list, name='list'),
    path('<uuid:order_id>/', views.order_detail, name='detail'),
    path('calculate-distance/', views.calculate_distance, name='calculate_distance'),
    path('calculate-delivery-fee/', views.calculate_delivery_fee_ajax, name='calculate_delivery_fee'),
    path('cancel/', views.cancel_order, name='cancel'),
    path('rate/', views.rate_order, name='rate'),
    # Carrinho
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
]
