from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import User
from orders.models import Order
import json

def user_register(request):
    """View para cadastro de usuários"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validações básicas
            if not all([data.get('email'), data.get('password'), data.get('first_name'), 
                       data.get('last_name'), data.get('address'), data.get('city'), 
                       data.get('state'), data.get('zip_code')]):
                return JsonResponse({
                    'success': False,
                    'message': 'Todos os campos obrigatórios devem ser preenchidos'
                }, status=400)
            
            # Verifica se o email já existe
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Este email já está cadastrado'
                }, status=400)
            
            # Cria o usuário
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data.get('phone_number', ''),
                address=data['address'],
                city=data['city'],
                state=data['state'],
                zip_code=data['zip_code'],
                latitude=data.get('latitude'),
                longitude=data.get('longitude')
            )
            
            # Faz login automático
            user = authenticate(username=data['email'], password=data['password'])
            if user:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Usuário cadastrado com sucesso!',
                    'user_id': user.id
                })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Dados inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao cadastrar usuário: {str(e)}'
            }, status=500)
    
    return render(request, 'users/register.html')

@login_required
def user_dashboard(request):
    """Dashboard do usuário"""
    user = request.user
    
    # Busca pedidos do usuário
    orders = Order.objects.filter(customer=user).order_by('-created_at')
    
    # Estatísticas básicas
    total_orders = orders.count()
    completed_orders = orders.filter(status='delivered').count()
    pending_orders = orders.filter(status__in=['pending', 'accepted', 'picked_up']).count()
    
    context = {
        'user': user,
        'orders': orders[:10],  # Últimos 10 pedidos
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
    }
    
    return render(request, 'users/dashboard.html', context)

@login_required
def user_profile(request):
    """Perfil do usuário"""
    user = request.user
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Atualiza dados do usuário
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.phone_number = data.get('phone_number', user.phone_number)
            user.address = data.get('address', user.address)
            user.city = data.get('city', user.city)
            user.state = data.get('state', user.state)
            user.zip_code = data.get('zip_code', user.zip_code)
            
            if data.get('latitude') and data.get('longitude'):
                user.latitude = data['latitude']
                user.longitude = data['longitude']
            
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Perfil atualizado com sucesso!'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Dados inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao atualizar perfil: {str(e)}'
            }, status=500)
    
    return render(request, 'users/profile.html', {'user': user})

@login_required
def user_orders(request):
    """Lista de pedidos do usuário"""
    user = request.user
    orders = Order.objects.filter(customer=user).order_by('-created_at')
    
    context = {
        'orders': orders,
        'user': user
    }
    
    return render(request, 'users/orders.html', context)

@login_required
def order_detail(request, order_id):
    """Detalhes de um pedido específico"""
    user = request.user
    order = get_object_or_404(Order, id=order_id, customer=user)
    
    context = {
        'order': order,
        'user': user
    }
    
    return render(request, 'users/order_detail.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def update_user_location(request):
    """Atualiza a localização do usuário"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not all([user_id, latitude, longitude]):
            return JsonResponse({
                'success': False,
                'message': 'Dados incompletos'
            }, status=400)
        
        user = get_object_or_404(User, id=user_id)
        user.latitude = latitude
        user.longitude = longitude
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Localização atualizada com sucesso!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao atualizar localização: {str(e)}'
        }, status=500)
