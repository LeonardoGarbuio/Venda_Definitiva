from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.conf import settings
from .models import Order, MenuItem, CartItem
from users.models import User
from motoboys.models import Motoboy
import json

def get_cart_items(request):
    """Obtém itens do carrinho baseado na sessão"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    return CartItem.objects.filter(session_key=session_key).select_related('menu_item')

def get_cart_total(request, delivery_address=None):
    """Calcula o total do carrinho com taxa de entrega baseada na distância"""
    cart_items = get_cart_items(request)
    subtotal = sum(float(item.total_price) for item in cart_items)
    
    # Calcula taxa de entrega baseada na distância
    delivery_fee = calculate_delivery_fee(delivery_address) if delivery_address else 5.00
    
    total = subtotal + delivery_fee
    return {
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': total,
        'distance_km': get_delivery_distance(delivery_address) if delivery_address else 0
    }

def calculate_delivery_fee(delivery_address):
    """Calcula taxa de entrega baseada na distância real"""
    if not delivery_address:
        return 5.00  # Taxa mínima
    
    distance_km = get_delivery_distance(delivery_address)
    
    # Taxa por km (R$ 2,50 por km)
    rate_per_km = 2.50
    # Taxa base mínima
    base_fee = 3.00
    
    delivery_fee = base_fee + (distance_km * rate_per_km)
    
    # Arredonda para 2 casas decimais
    return round(delivery_fee, 2)

def get_delivery_distance(delivery_address):
    """Calcula distância real entre restaurante e endereço de entrega"""
    if not delivery_address:
        return 0
    
    # Coordenadas do restaurante (exemplo: Lisboa)
    restaurant_coords = {
        'lat': 38.7223,
        'lng': -9.1393,
        'address': 'Rua Augusta, 123, Baixa, Lisboa'
    }
    
    # Simula cálculo de rota real usando OpenStreetMap
    # Em produção, você usaria a API do OSRM ou Google Maps Directions
    
    # Coordenadas do endereço de entrega (baseado no CEP)
    delivery_coords = get_coordinates_from_address(delivery_address)
    
    if not delivery_coords:
        return 0
    
    # Calcula distância em linha reta primeiro
    straight_distance = calculate_straight_line_distance(
        restaurant_coords['lat'], restaurant_coords['lng'],
        delivery_coords['lat'], delivery_coords['lng']
    )
    
    # Aplica fator de correção para rotas reais (considera curvas, vias, etc.)
    # Fator típico: 1.3 a 1.5 (30-50% a mais que distância em linha reta)
    route_factor = 1.4
    
    real_distance = straight_distance * route_factor
    
    return round(real_distance, 2)

def get_coordinates_from_address(address):
    """Obtém coordenadas do endereço baseado no CEP"""
    # Mapeamento de CEPs para coordenadas (simulado)
    cep_coordinates = {
        '1000': {'lat': 38.7223, 'lng': -9.1393, 'city': 'Lisboa'},
        '2000': {'lat': 39.2362, 'lng': -8.6869, 'city': 'Santarém'},
        '3000': {'lat': 40.2033, 'lng': -8.4103, 'city': 'Coimbra'},
        '4000': {'lat': 41.1579, 'lng': -8.6291, 'city': 'Porto'},
        '5000': {'lat': 41.2956, 'lng': -7.7463, 'city': 'Vila Real'},
        '6000': {'lat': 39.8222, 'lng': -7.4909, 'city': 'Castelo Branco'},
        '7000': {'lat': 38.5714, 'lng': -7.9135, 'city': 'Évora'},
        '8000': {'lat': 37.0194, 'lng': -7.9304, 'city': 'Faro'},
        '9000': {'lat': 32.6669, 'lng': -16.9241, 'city': 'Funchal'}
    }
    
    # Extrai CEP do endereço
    import re
    cep_match = re.search(r'(\d{4})', address)
    if cep_match:
        cep_prefix = cep_match.group(1)
        return cep_coordinates.get(cep_prefix)
    
    return None

def calculate_straight_line_distance(lat1, lng1, lat2, lng2):
    """Calcula distância em linha reta entre dois pontos (fórmula de Haversine)"""
    import math
    
    R = 6371  # Raio da Terra em km
    
    lat1, lng1 = math.radians(lat1), math.radians(lng1)
    lat2, lng2 = math.radians(lat2), math.radians(lng2)
    
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    distance = R * c
    
    return distance

@csrf_exempt
def add_to_cart(request):
    """Adiciona item ao carrinho"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = data.get('quantity', 1)
            
            menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
            
            # Garante que a sessão existe
            if not request.session.session_key:
                request.session.create()
            
            # Adiciona ou atualiza item no carrinho
            cart_item, created = CartItem.objects.get_or_create(
                session_key=request.session.session_key,
                menu_item=menu_item,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity = int(cart_item.quantity) + int(quantity)
                cart_item.save()
            
            cart_data = get_cart_total(request)
            cart_data['item_count'] = get_cart_items(request).count()
            
            return JsonResponse({
                'success': True,
                'message': f'{menu_item.name} adicionado ao carrinho!',
                'cart': cart_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao adicionar item: {str(e)}'
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

@csrf_exempt
def update_cart_item(request):
    """Atualiza quantidade de item no carrinho"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = data.get('quantity', 1)
            
            cart_item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
            
            if quantity <= 0:
                cart_item.delete()
                message = 'Item removido do carrinho'
            else:
                cart_item.quantity = quantity
                cart_item.save()
                message = 'Carrinho atualizado'
            
            cart_data = get_cart_total(request)
            cart_data['item_count'] = get_cart_items(request).count()
            
            return JsonResponse({
                'success': True,
                'message': message,
                'cart': cart_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao atualizar carrinho: {str(e)}'
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

@csrf_exempt
def remove_from_cart(request):
    """Remove item do carrinho"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            
            cart_item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
            item_name = cart_item.menu_item.name
            cart_item.delete()
            
            cart_data = get_cart_total(request)
            cart_data['item_count'] = get_cart_items(request).count()
            
            return JsonResponse({
                'success': True,
                'message': f'{item_name} removido do carrinho',
                'cart': cart_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao remover item: {str(e)}'
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

def create_order(request):
    """View para criação de pedidos"""
    # Obtém itens do carrinho
    cart_items = get_cart_items(request)
    cart_total = get_cart_total(request)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validações básicas
            required_fields = ['pickup_address', 'delivery_address', 'description', 'base_price', 'customer_name', 'customer_email', 'customer_phone']
            
            if not all(data.get(field) for field in required_fields):
                return JsonResponse({
                    'success': False,
                    'message': 'Todos os campos obrigatórios devem ser preenchidos'
                }, status=400)
            
            # Verifica se há itens no carrinho
            if not cart_items.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Carrinho vazio'
                }, status=400)
            
            # Cria ou obtém o usuário baseado no email
            customer_email = data['customer_email']
            customer, created = User.objects.get_or_create(
                email=customer_email,
                defaults={
                    'username': customer_email,
                    'first_name': data['customer_name'].split()[0] if data['customer_name'] else '',
                    'last_name': ' '.join(data['customer_name'].split()[1:]) if len(data['customer_name'].split()) > 1 else '',
                    'phone_number': data['customer_phone'],
                    'address': data['delivery_address'],
                }
            )
            
            # Cria o pedido
            order = Order.objects.create(
                customer=customer,
                pickup_address=data['pickup_address'],
                pickup_latitude=data.get('pickup_latitude'),
                pickup_longitude=data.get('pickup_longitude'),
                delivery_address=data['delivery_address'],
                delivery_latitude=data.get('delivery_latitude'),
                delivery_longitude=data.get('delivery_longitude'),
                description=data['description'],
                weight=data.get('weight', 0.5),
                dimensions=data.get('dimensions', 'Padrão'),
                is_fragile=data.get('is_fragile', False),
                priority=data.get('priority', 'normal'),
                base_price=cart_total['total'],  # Usa o total do carrinho
                distance_km=data.get('distance_km', 0)
            )
            
            # Calcula preço final se houver distância
            if order.distance_km and order.distance_km > 0:
                order.calculate_final_price()
            else:
                # Se não há distância, o preço final é igual ao preço base
                order.final_price = order.base_price
                order.save(update_fields=['final_price'])
            
            # Limpa o carrinho após criar o pedido
            cart_items.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Pedido criado com sucesso!',
                'order_id': order.id,
                'order_number': order.order_number
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Dados inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao criar pedido: {str(e)}'
            }, status=500)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total
    }
    return render(request, 'orders/create_order.html', context)

@login_required
def order_list(request):
    """Lista de pedidos (para admin)"""
    # Verifica se é staff
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado.')
        return redirect('user_dashboard')
    
    # Filtros
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search_query = request.GET.get('search', '')
    
    orders = Order.objects.all()
    
    # Aplica filtros
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    if priority_filter:
        orders = orders.filter(priority=priority_filter)
    
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(customer__email__icontains=search_query) |
            Q(pickup_address__icontains=search_query) |
            Q(delivery_address__icontains=search_query)
        )
    
    orders = orders.order_by('-created_at')
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'priority_choices': Order.PRIORITY_CHOICES,
        'current_filters': {
            'status': status_filter,
            'priority': priority_filter,
            'search': search_query
        }
    }
    
    return render(request, 'orders/order_list.html', context)

@login_required
def order_detail(request, order_id):
    """Detalhes de um pedido específico"""
    # Verifica se é staff ou se é o cliente do pedido
    order = get_object_or_404(Order, id=order_id)
    
    if not request.user.is_staff and order.customer != request.user:
        messages.error(request, 'Acesso negado.')
        return redirect('user_dashboard')
    
    context = {
        'order': order
    }
    
    return render(request, 'orders/order_detail.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def calculate_delivery_fee_ajax(request):
    """Calcula taxa de entrega baseada no endereço de entrega"""
    try:
        data = json.loads(request.body)
        delivery_address = data.get('delivery_address')
        
        if not delivery_address:
            return JsonResponse({
                'success': False,
                'message': 'Endereço de entrega é obrigatório'
            }, status=400)
        
        # Calcula distância e taxa
        distance_km = get_delivery_distance(delivery_address)
        delivery_fee = calculate_delivery_fee(delivery_address)
        
        # Obtém dados do carrinho
        cart_data = get_cart_total(request, delivery_address)
        
        return JsonResponse({
            'success': True,
            'distance_km': distance_km,
            'delivery_fee': delivery_fee,
            'cart_total': cart_data,
            'route_info': {
                'restaurant_address': 'Rua Augusta, 123, Baixa, Lisboa',
                'delivery_address': delivery_address,
                'estimated_time': f'{int(distance_km * 2)}-{int(distance_km * 3)} min'
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao calcular taxa de entrega: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def calculate_distance(request):
    """Calcula distância entre dois pontos (simulado)"""
    try:
        data = json.loads(request.body)
        pickup_lat = data.get('pickup_latitude')
        pickup_lng = data.get('pickup_longitude')
        delivery_lat = data.get('delivery_latitude')
        delivery_lng = data.get('delivery_longitude')
        
        if not all([pickup_lat, pickup_lng, delivery_lat, delivery_lng]):
            return JsonResponse({
                'success': False,
                'message': 'Coordenadas incompletas'
            }, status=400)
        
        # Cálculo simples de distância (fórmula de Haversine)
        import math
        
        R = 6371  # Raio da Terra em km
        
        lat1, lon1 = math.radians(float(pickup_lat)), math.radians(float(pickup_lng))
        lat2, lon2 = math.radians(float(delivery_lat)), math.radians(float(delivery_lng))
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        distance = R * c
        
        # Calcula preço estimado (R$ 2,50 por km + taxa base de R$ 5,00)
        base_price = 5.00
        estimated_price = base_price + (distance * 2.50)
        
        return JsonResponse({
            'success': True,
            'distance_km': round(distance, 2),
            'estimated_price': round(estimated_price, 2),
            'base_price': base_price
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao calcular distância: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def cancel_order(request):
    """Cancela um pedido"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        user_id = data.get('user_id')
        
        if not all([order_id, user_id]):
            return JsonResponse({
                'success': False,
                'message': 'Dados incompletos'
            }, status=400)
        
        order = get_object_or_404(Order, id=order_id)
        user = get_object_or_404(User, id=user_id)
        
        # Verifica se o usuário pode cancelar o pedido
        if order.customer != user and not user.is_staff:
            return JsonResponse({
                'success': False,
                'message': 'Acesso negado'
            }, status=403)
        
        # Verifica se o pedido pode ser cancelado
        if order.status not in ['pending', 'accepted']:
            return JsonResponse({
                'success': False,
                'message': 'Este pedido não pode ser cancelado'
            }, status=400)
        
        # Cancela o pedido
        order.status = 'cancelled'
        order.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Pedido cancelado com sucesso!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao cancelar pedido: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def rate_order(request):
    """Avalia um pedido entregue"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        user_id = data.get('user_id')
        rating = data.get('rating')
        feedback = data.get('feedback', '')
        
        if not all([order_id, user_id, rating]):
            return JsonResponse({
                'success': False,
                'message': 'Dados incompletos'
            }, status=400)
        
        # Valida rating
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError("Rating deve estar entre 1 e 5")
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Rating inválido'
            }, status=400)
        
        order = get_object_or_404(Order, id=order_id)
        user = get_object_or_404(User, id=user_id)
        
        # Verifica se o usuário é o cliente do pedido
        if order.customer != user:
            return JsonResponse({
                'success': False,
                'message': 'Acesso negado'
            }, status=403)
        
        # Verifica se o pedido foi entregue
        if order.status != 'delivered':
            return JsonResponse({
                'success': False,
                'message': 'Apenas pedidos entregues podem ser avaliados'
            }, status=400)
        
        # Atualiza avaliação
        order.rating = rating
        order.feedback = feedback
        order.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Pedido avaliado com sucesso!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao avaliar pedido: {str(e)}'
        }, status=500)
