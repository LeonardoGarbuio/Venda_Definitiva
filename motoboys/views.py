from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.conf import settings
from .models import Motoboy
from orders.models import Order
from users.models import User
import json

def motoboy_login(request):
    """View para login de motoboys com redirecionamento automático"""
    # Se o usuário já está logado e é um motoboy, redireciona para o dashboard
    if request.user.is_authenticated:
        try:
            motoboy = Motoboy.objects.get(user=request.user)
            return redirect('motoboys:dashboard')
        except Motoboy.DoesNotExist:
            pass
    
    # Verifica se há cookie de "lembrar dispositivo"
    remember_token = request.COOKIES.get('motoboy_remember')
    if remember_token:
        try:
            # Decodifica o token e verifica se é válido
            import base64
            import json
            from django.utils import timezone
            from datetime import timedelta
            
            token_data = json.loads(base64.b64decode(remember_token).decode())
            user_id = token_data.get('user_id')
            expiry = token_data.get('expiry')
            
            # Verifica se o token não expirou
            if expiry and timezone.now().isoformat() < expiry:
                user = User.objects.get(id=user_id)
                motoboy = Motoboy.objects.get(user=user)
                
                # Faz login automático
                login(request, user)
                return redirect('motoboys:dashboard')
        except (ValueError, json.JSONDecodeError, User.DoesNotExist, Motoboy.DoesNotExist):
            # Token inválido, remove o cookie
            pass
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            remember_me = data.get('remember_me', False)
            device_id = data.get('device_id')  # Novo campo
            print(f"=== DEBUG LOGIN ===")
            print(f"Email: {email}")
            print(f"Device ID recebido: {device_id}")
            print(f"Tipo do device_id: {type(device_id)}")
            print(f"Dados completos: {data}")
            print(f"==================")
            
            if not email or not password:
                return JsonResponse({
                    'success': False,
                    'message': 'Email e senha são obrigatórios'
                }, status=400)
            
            # Autentica o usuário
            user = authenticate(username=email, password=password)
            
            if user is not None:
                # Verifica se o usuário é um motoboy
                try:
                    motoboy = Motoboy.objects.get(user=user)
                    
                    # Salva o device_id se fornecido
                    if device_id:
                        try:
                            print(f"=== DEBUG SALVAR DEVICE_ID ===")
                            print(f"Device ID a salvar: {device_id}")
                            print(f"Tipo do device_id: {type(device_id)}")
                            print(f"Device IDs atuais: {motoboy.device_ids}")
                            print(f"Tipo dos device_ids: {type(motoboy.device_ids)}")
                            
                            current_device_ids = motoboy.device_ids or []
                            print(f"Lista atual: {current_device_ids}")
                            print(f"Tipo da lista: {type(current_device_ids)}")
                            
                            if device_id not in current_device_ids:
                                current_device_ids.append(device_id)
                                print(f"Nova lista: {current_device_ids}")
                                motoboy.device_ids = current_device_ids
                                motoboy.save()
                                print(f"✅ Device ID {device_id} salvo para motoboy {motoboy.full_name}")
                                print(f"✅ Device IDs finais: {motoboy.device_ids}")
                            else:
                                print(f"⚠️ Device ID {device_id} já existe para motoboy {motoboy.full_name}")
                            print(f"===============================")
                        except Exception as e:
                            print(f"❌ Erro ao salvar device_id: {e}")
                            print(f"❌ Tipo do erro: {type(e)}")
                            import traceback
                            traceback.print_exc()
                            pass
                    else:
                        print(f"⚠️ Nenhum device_id fornecido para salvar")
                    
                    login(request, user)
                    
                    # Define cookie para "lembrar dispositivo" se solicitado
                    response = JsonResponse({
                        'success': True,
                        'message': 'Login realizado com sucesso!',
                        'redirect': '/motoboys/dashboard/'
                    })
                    
                    if remember_me:
                        # Cria token de "lembrar dispositivo" (30 dias)
                        import base64
                        import json
                        from django.utils import timezone
                        from datetime import timedelta
                        
                        token_data = {
                            'user_id': user.id,
                            'expiry': (timezone.now() + timedelta(days=30)).isoformat()
                        }
                        token = base64.b64encode(json.dumps(token_data).encode()).decode()
                        
                        response.set_cookie('motoboy_remember', token, max_age=30*24*60*60, httponly=True, samesite='Lax')
                    
                    return response
                except Motoboy.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'message': 'Este usuário não é um motoboy cadastrado'
                    }, status=400)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Email ou senha incorretos'
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Dados inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro no login: {str(e)}'
            }, status=500)
    
    return render(request, 'motoboys/login.html')

import hashlib
import json

def check_device_status(request):
    """Verifica o status do dispositivo usando identificadores únicos como grandes empresas"""
    
    print(f"=== DEBUG CHECK_DEVICE_STATUS ===")
    print(f"Usuário autenticado: {request.user.is_authenticated}")
    
    # 1. Verifica se há uma sessão ativa
    if request.user.is_authenticated:
        try:
            motoboy = Motoboy.objects.get(user=request.user)
            print(f"Usuário logado: {motoboy.full_name}")
            return JsonResponse({
                'is_new_device': False,
                'show_register': False,
                'show_login': True,
                'user_name': motoboy.user.first_name or motoboy.user.username
            })
        except Motoboy.DoesNotExist:
            print("Usuário logado mas não é motoboy")
            pass
    
    # 2. Tenta obter o device_id do frontend (localStorage)
    device_id = request.GET.get('device_id')
    print(f"Device ID recebido do frontend: {device_id}")
    
    # 3. Se recebeu device_id, verifica se já existe cadastro
    if device_id and device_id.strip():
        print(f"🔍 VERIFICANDO DEVICE_ID EXISTENTE: {device_id}")
        existing_motoboy = check_existing_device_registration(device_id, request)
        
        if existing_motoboy:
            print(f"✅ Dispositivo já cadastrado para: {existing_motoboy.full_name}")
            return JsonResponse({
                'is_new_device': False,
                'show_register': False,
                'show_login': True,
                'message': 'Dispositivo já cadastrado',
                'device_id': device_id
            })
        else:
            print(f"❌ Device_id não encontrado no banco, mas foi enviado pelo frontend")
            print(f"❌ Isso indica um problema de sincronização")
    
    # 4. IMPORTANTE: NÃO gera device_id automaticamente!
    # Só gera quando o usuário realmente criar a conta
    if not device_id or not device_id.strip():
        print(f"🆕 FRONTEND NÃO ENVIOU DEVICE_ID")
        print(f"🆕 NÃO GERANDO AUTOMATICAMENTE - aguardando criação da conta")
        # Retorna sem device_id para forçar cadastro
        return JsonResponse({
            'is_new_device': True,
            'show_register': True,
            'show_login': False,
            'device_id': None,
            'message': 'Dispositivo novo - aguardando cadastro'
        })
    
    # 5. Se chegou aqui, tem device_id mas não encontrou cadastro
    print(f"🔄 REUTILIZANDO DEVICE_ID ENVIADO PELO FRONTEND: {device_id}")
    
    # 6. Mostra cadastro para dispositivo novo
    print(f"📝 Dispositivo novo, mostrando cadastro")
    print(f"=== FIM DEBUG ===")
    return JsonResponse({
        'is_new_device': True,
        'show_register': True,
        'show_login': False,
        'device_id': device_id
    })

def generate_device_id(request):
    """Gera um ID único para o dispositivo baseado em múltiplos fatores"""
    
    print(f"🚀 === INICIANDO GENERATE_DEVICE_ID ===")
    
    # Coleta informações do dispositivo
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    accept_encoding = request.META.get('HTTP_ACCEPT_ENCODING', '')
    
    # IP do usuário (considerando proxies)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        print(f"🌐 IP detectado via X-Forwarded-For: {ip}")
    else:
        ip = request.META.get('REMOTE_ADDR', '')
        print(f"🌐 IP direto: {ip}")
    
    # Informações adicionais para maior unicidade
    host = request.META.get('HTTP_HOST', '')
    referer = request.META.get('HTTP_REFERER', '')
    
    print(f"📋 DADOS COLETADOS:")
    print(f"  IP: {ip}")
    print(f"  User-Agent: {user_agent[:100]}...")
    print(f"  Accept-Language: {accept_language}")
    print(f"  Accept-Encoding: {accept_encoding}")
    print(f"  Host: {host}")
    print(f"  Referer: {referer}")
    
    # Cria um hash único baseado em múltiplos fatores
    device_string = f"{ip}|{user_agent}|{accept_language}|{accept_encoding}|{host}|{referer}"
    
    print(f"🔍 DEVICE STRING CRIADA:")
    print(f"  String: {device_string[:200]}...")
    print(f"  Tamanho: {len(device_string)}")
    
    # Gera o hash SHA256
    import hashlib
    device_hash = hashlib.sha256(device_string.encode()).hexdigest()[:16]
    
    print(f"🔢 HASH GERADO:")
    print(f"  Hash completo (SHA256): {hashlib.sha256(device_string.encode()).hexdigest()}")
    print(f"  Hash truncado (16 chars): {device_hash}")
    print(f"  Tamanho do hash: {len(device_hash)}")
    
    print(f"🚀 === FIM GENERATE_DEVICE_ID ====")
    return device_hash

def check_existing_device_registration(device_id, request):
    """Verifica se já existe um cadastro para este dispositivo"""
    
    print(f"🚀 === INICIANDO CHECK_EXISTING_DEVICE_REGISTRATION ===")
    print(f"🔍 PARÂMETROS RECEBIDOS:")
    print(f"  device_id: {device_id}")
    print(f"  Tipo do device_id: {type(device_id)}")
    print(f"  Tamanho: {len(device_id) if device_id else 0}")
    print(f"  Request: {request}")
    
    # 1. Verifica se já existe um motoboy com este device_id
    try:
        print(f"🔍 INICIANDO BUSCA NO BANCO...")
        
        # SQLite não suporta contains em JSONField, vamos usar uma abordagem diferente
        motoboys = Motoboy.objects.all()
        total_motoboys = motoboys.count()
        print(f"📊 TOTAL DE MOTOBOYS NO BANCO: {total_motoboys}")
        
        if total_motoboys == 0:
            print(f"❌ NENHUM MOTOBOY NO BANCO!")
            print(f"🚀 === FIM CHECK_EXISTING_DEVICE_REGISTRATION (BANCO VAZIO) ====")
            return None
        
        print(f"🔍 VERIFICANDO CADA MOTOBOY...")
        
        for i, motoboy in enumerate(motoboys):
            print(f"  📋 MOTOBOY {i+1}/{total_motoboys}:")
            print(f"    Nome: {motoboy.full_name}")
            print(f"    Email: {motoboy.user.email}")
            print(f"    Device IDs: {motoboy.device_ids}")
            print(f"    Tipo dos device_ids: {type(motoboy.device_ids)}")
            
            if motoboy.device_ids:
                print(f"    ✅ TEM DEVICE_IDS, VERIFICANDO...")
                device_ids_count = len(motoboy.device_ids)
                print(f"    📊 Total de device_ids: {device_ids_count}")
                
                for j, stored_id in enumerate(motoboy.device_ids):
                    print(f"      🔍 DEVICE_ID {j+1}/{device_ids_count}:")
                    print(f"        Valor: '{stored_id}'")
                    print(f"        Tipo: {type(stored_id)}")
                    print(f"        Tamanho: {len(stored_id) if stored_id else 0}")
                    print(f"        Comparando com: '{device_id}'")
                    print(f"        São iguais? {device_id == stored_id}")
                    print(f"        Comparação detalhada:")
                    print(f"          device_id == stored_id: {device_id == stored_id}")
                    print(f"          device_id is stored_id: {device_id is stored_id}")
                    print(f"          len(device_id) == len(stored_id): {len(device_id) == len(stored_id) if stored_id else False}")
                    
                    if device_id == stored_id:
                        print(f"        🎯 MATCH ENCONTRADO!")
                        print(f"        ✅ ENCONTROU! Motoboy: {motoboy.full_name}")
                        print(f"🚀 === FIM CHECK_EXISTING_DEVICE_REGISTRATION (MATCH) ====")
                        return motoboy
                    else:
                        print(f"        ❌ NÃO É IGUAL")
            else:
                print(f"    ❌ SEM DEVICE_IDS")
        
        print(f"❌ NENHUM MOTOBOY ENCONTRADO COM DEVICE_ID: {device_id}")
        print(f"📊 RESUMO DA BUSCA:")
        print(f"  Total de motoboys verificados: {total_motoboys}")
        print(f"  Device ID procurado: {device_id}")
        print(f"  Device IDs encontrados no banco:")
        
        for motoboy in motoboys:
            if motoboy.device_ids:
                for stored_id in motoboy.device_ids:
                    print(f"    - {stored_id} (de {motoboy.full_name})")
        
        print("===============================")
        print(f"🚀 === FIM CHECK_EXISTING_DEVICE_REGISTRATION (NÃO ENCONTRADO) ====")
        return None
        
    except Exception as e:
        print(f"❌ ERRO AO VERIFICAR DEVICE_ID:")
        print(f"  Erro: {e}")
        print(f"  Tipo do erro: {type(e)}")
        print(f"  Mensagem: {str(e)}")
        import traceback
        print(f"  Stack trace: {traceback.format_exc()}")
        print(f"🚀 === FIM CHECK_EXISTING_DEVICE_REGISTRATION (ERRO) ====")
        return None

def check_motoboy_status(request):
    """Verifica se o usuário já tem cadastro de motoboy"""
    email = request.GET.get('email')
    
    if not email:
        return JsonResponse({
            'has_account': False,
            'message': 'Email não fornecido'
        })
    
    # Verifica se já existe um usuário com este email
    try:
        user = User.objects.get(email=email)
        # Verifica se é um motoboy
        try:
            motoboy = Motoboy.objects.get(user=user)
            return JsonResponse({
                'has_account': True,
                'message': 'Você já tem uma conta de motoboy',
                'redirect': '/motoboys/login/'
            })
        except Motoboy.DoesNotExist:
            # Usuário existe mas não é motoboy
            return JsonResponse({
                'has_account': False,
                'message': 'Email disponível para cadastro'
            })
    except User.DoesNotExist:
        # Email não existe, pode cadastrar
        return JsonResponse({
            'has_account': False,
            'message': 'Email disponível para cadastro'
        })

def motoboy_register(request):
    """View para cadastro de motoboys"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            device_id = data.get('device_id')  # Pega o device_id do JSON
            
            print(f"=== DEBUG MOTOBOY_REGISTER ===")
            print(f"Device ID recebido: {device_id}")
            print(f"Tipo do device_id: {type(device_id)}")
            print(f"Dados completos: {data}")
            print(f"=============================")
            
            # Validações básicas
            required_fields = ['email', 'password', 'full_name', 'phone_number', 
                             'document_type', 'document_number', 'vehicle_model', 
                             'vehicle_plate', 'vehicle_year', 'vehicle_color']
            
            if not all(data.get(field) for field in required_fields):
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
            
            # Verifica se o documento já existe
            if Motoboy.objects.filter(document_number=data['document_number']).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Este documento já está cadastrado'
                }, status=400)
            
            # Verifica se a placa já existe
            if Motoboy.objects.filter(vehicle_plate=data['vehicle_plate']).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Esta placa já está cadastrada'
                }, status=400)
            
            # Cria o usuário primeiro
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['full_name'].split()[0],
                last_name=' '.join(data['full_name'].split()[1:]) if len(data['full_name'].split()) > 1 else '',
                is_staff=True  # Motoboys são staff para acessar o sistema
            )
            
            # Cria o motoboy
            print(f"🔧 SALVANDO MOTOBOY NO BANCO...")
            print(f"🔧 Device ID a salvar: {device_id}")
            print(f"🔧 Device IDs array: {[device_id] if device_id else []}")
            
            motoboy = Motoboy.objects.create(
                user=user,
                full_name=data['full_name'],
                phone_number=data['phone_number'],
                document_type=data['document_type'],
                document_number=data['document_number'],
                vehicle_model=data['vehicle_model'],
                vehicle_plate=data['vehicle_plate'],
                vehicle_year=data['vehicle_year'],
                vehicle_color=data['vehicle_color'],
                status='offline',  # Começa offline
                device_ids=[device_id] if device_id else []  # Salva o device_id
            )
            
            print(f"✅ MOTOBOY SALVO COM SUCESSO!")
            print(f"✅ ID do motoboy: {motoboy.id}")
            print(f"✅ Device IDs salvos: {motoboy.device_ids}")
            print(f"✅ Tipo dos device_ids: {type(motoboy.device_ids)}")
            
            # Faz login automático
            user = authenticate(username=data['email'], password=data['password'])
            if user:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Motoboy cadastrado com sucesso!',
                    'motoboy_id': motoboy.id
                })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Dados inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao cadastrar motoboy: {str(e)}'
            }, status=500)
    
    return render(request, 'motoboys/register.html')

@login_required
def motoboy_dashboard(request):
    """Dashboard do motoboy"""
    try:
        motoboy = Motoboy.objects.get(user=request.user)
    except Motoboy.DoesNotExist:
        messages.error(request, 'Perfil de motoboy não encontrado.')
        return redirect('motoboy_register')
    
    # Busca pedidos disponíveis (pendentes)
    available_orders = Order.objects.filter(
        status='pending'
    ).exclude(
        motoboy__isnull=False
    ).order_by('-priority', '-created_at')
    
    # Busca pedidos do motoboy
    my_orders = Order.objects.filter(
        motoboy=motoboy
    ).exclude(
        status__in=['delivered', 'cancelled', 'failed']
    ).order_by('-created_at')
    
    # Estatísticas
    total_deliveries = motoboy.total_deliveries
    successful_deliveries = motoboy.successful_deliveries
    success_rate = motoboy.get_success_rate()
    
    context = {
        'motoboy': motoboy,
        'available_orders': available_orders[:20],  # Primeiros 20 pedidos
        'my_orders': my_orders,
        'total_deliveries': total_deliveries,
        'successful_deliveries': successful_deliveries,
        'success_rate': success_rate,
    }
    
    return render(request, 'motoboys/dashboard.html', context)

@login_required
def motoboy_logout(request):
    """Logout do motoboy"""
    from django.contrib.auth import logout
    from django.http import JsonResponse
    
    logout(request)
    
    # Remove o cookie de "lembrar dispositivo"
    response = JsonResponse({
        'success': True,
        'message': 'Logout realizado com sucesso!',
        'redirect': '/motoboys/login/'
    })
    response.delete_cookie('motoboy_remember')
    
    return response

@login_required
def motoboy_profile(request):
    """Perfil do motoboy"""
    try:
        motoboy = Motoboy.objects.get(user=request.user)
    except Motoboy.DoesNotExist:
        messages.error(request, 'Perfil de motoboy não encontrado.')
        return redirect('motoboy_register')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Atualiza dados do motoboy
            motoboy.full_name = data.get('full_name', motoboy.full_name)
            motoboy.phone_number = data.get('phone_number', motoboy.phone_number)
            motoboy.vehicle_model = data.get('vehicle_model', motoboy.vehicle_model)
            motoboy.vehicle_color = data.get('vehicle_color', motoboy.vehicle_color)
            
            motoboy.save()
            
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
    
    return render(request, 'motoboys/profile.html', {'motoboy': motoboy})

@login_required
def motoboy_orders(request):
    """Lista de pedidos do motoboy"""
    try:
        motoboy = Motoboy.objects.get(user=request.user)
    except Motoboy.DoesNotExist:
        messages.error(request, 'Perfil de motoboy não encontrado.')
        return redirect('motoboy_register')
    
    # Busca todos os pedidos do motoboy
    orders = Order.objects.filter(motoboy=motoboy).order_by('-created_at')
    
    context = {
        'motoboy': motoboy,
        'orders': orders
    }
    
    return render(request, 'motoboys/orders.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def accept_order(request):
    """Motoboy aceita um pedido"""
    try:
        # Debug: Verificar autenticação
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")
        
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        if not order_id:
            return JsonResponse({
                'success': False,
                'message': 'ID do pedido é obrigatório'
            }, status=400)
        
        # Busca o motoboy
        try:
            motoboy = Motoboy.objects.get(user=request.user)
            print(f"Motoboy found: {motoboy.full_name}, Status: {motoboy.status}")
        except Motoboy.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Perfil de motoboy não encontrado'
            }, status=404)
        
        # Busca o pedido
        try:
            order = Order.objects.get(id=order_id, status='pending')
            print(f"Order found: {order.order_number}")
        except Order.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Pedido não encontrado ou já foi aceito'
            }, status=404)
        
        # Verifica se o motoboy está disponível
        print(f"Motoboy status check: {motoboy.status} == 'available' ? {motoboy.status == 'available'}")
        if motoboy.status != 'available':
            return JsonResponse({
                'success': False,
                'message': f'Você precisa estar disponível para aceitar pedidos. Status atual: {motoboy.status}'
            }, status=400)
        
        # Aceita o pedido
        order.motoboy = motoboy
        order.status = 'accepted'
        order.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Pedido #{order.order_number} aceito com sucesso!',
            'order': {
                'id': order.id,
                'order_number': order.order_number,
                'delivery_address': order.delivery_address,
                'customer_name': f"{order.customer.first_name} {order.customer.last_name}",
                'customer_phone': order.customer.phone_number
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
            'message': f'Erro ao aceitar pedido: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def update_order_status(request):
    """Atualiza status do pedido"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_status = data.get('status')
        
        if not all([order_id, new_status]):
            return JsonResponse({
                'success': False,
                'message': 'ID do pedido e status são obrigatórios'
            }, status=400)
        
        # Valida status
        valid_statuses = ['picked_up', 'in_transit', 'delivered']
        if new_status not in valid_statuses:
            return JsonResponse({
                'success': False,
                'message': 'Status inválido'
            }, status=400)
        
        # Busca o motoboy
        try:
            motoboy = Motoboy.objects.get(user=request.user)
        except Motoboy.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Perfil de motoboy não encontrado'
            }, status=404)
        
        # Busca o pedido
        try:
            order = Order.objects.get(id=order_id, motoboy=motoboy)
        except Order.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Pedido não encontrado'
            }, status=404)
        
        # Atualiza status
        order.status = new_status
        order.save()
        
        # Se foi entregue, atualiza estatísticas do motoboy
        if new_status == 'delivered':
            motoboy.total_deliveries += 1
            motoboy.successful_deliveries += 1
            motoboy.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Status atualizado para: {dict(Order.STATUS_CHOICES)[new_status]}',
            'order': {
                'id': order.id,
                'order_number': order.order_number,
                'status': new_status,
                'status_display': dict(Order.STATUS_CHOICES)[new_status]
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
            'message': f'Erro ao atualizar status: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def update_motoboy_location(request):
    """Atualiza a localização do motoboy"""
    try:
        data = json.loads(request.body)
        motoboy_id = data.get('motoboy_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not all([motoboy_id, latitude, longitude]):
            return JsonResponse({
                'success': False,
                'message': 'Dados incompletos'
            }, status=400)
        
        motoboy = get_object_or_404(Motoboy, id=motoboy_id)
        motoboy.update_location(latitude, longitude)
        
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

@csrf_exempt
@require_http_methods(["POST"])
def update_motoboy_status(request):
    """Atualiza o status do motoboy"""
    try:
        data = json.loads(request.body)
        motoboy_id = data.get('motoboy_id')
        status = data.get('status')
        
        if not all([motoboy_id, status]):
            return JsonResponse({
                'success': False,
                'message': 'Dados incompletos'
            }, status=400)
        
        if status not in ['available', 'busy', 'offline']:
            return JsonResponse({
                'success': False,
                'message': 'Status inválido'
            }, status=400)
        
        motoboy = get_object_or_404(Motoboy, id=motoboy_id)
        motoboy.status = status
        motoboy.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Status atualizado para {status}',
            'status': status
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao atualizar status: {str(e)}'
        }, status=500)


