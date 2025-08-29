from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from core.models import Category, Product
import json

def home(request):
    """Página inicial com cardápio"""
    # Carrega categorias e produtos do banco de dados
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    products = Product.objects.filter(is_available=True).order_by('category__order', 'order', 'name')
    
    # Agrupa produtos por categoria
    menu_data = {}
    for category in categories:
        menu_data[category] = products.filter(category=category)
    
    context = {
        'categories': categories,
        'products': products,
        'menu_data': menu_data
    }
    return render(request, 'core/home.html', context)

def login(request):
    """Página de login administrativo"""
    print("🔍 === DEBUG LOGIN ===")
    print(f"📊 Request method: {request.method}")
    print(f"📊 Request path: {request.path}")
    print(f"📊 Session ID: {request.session.session_key}")
    print(f"📊 Session data: {dict(request.session)}")
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            print(f"📊 Email recebido: {email}")
            print(f"📊 Password recebido: {password}")
            
            # Credenciais fixas que você pode alterar
            ADMIN_EMAIL = 'admin@motodelivery.com'
            ADMIN_PASSWORD = 'admin123'
            
            # Verificar credenciais
            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                print("✅ Credenciais válidas, criando sessão...")
                # Criar sessão
                request.session['admin_logged_in'] = True
                request.session['admin_email'] = email
                
                # Forçar salvamento da sessão
                request.session.save()
                
                print(f"✅ Sessão criada: {dict(request.session)}")
                print(f"✅ Session key: {request.session.session_key}")
                
                # Retornar dados para criar sessão no localStorage
                return JsonResponse({
                    'success': True, 
                    'redirect': '/admin_dashboard/',
                    'session_data': {
                        'loginTime': timezone.now().isoformat(),
                        'email': email
                    }
                })
            else:
                print("❌ Credenciais inválidas")
                return JsonResponse({'success': False, 'message': 'Email ou senha incorretos.'})
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return JsonResponse({'success': False, 'message': 'Erro no servidor.'})
    
    print("📄 Renderizando página de login...")
    return render(request, 'core/login.html')

def admin_dashboard(request):
    """Dashboard administrativo"""
    print("🔍 === DEBUG ADMIN_DASHBOARD ===")
    print(f"📊 Request method: {request.method}")
    print(f"📊 Request path: {request.path}")
    print(f"📊 Session ID: {request.session.session_key}")
    print(f"📊 Session data: {dict(request.session)}")
    print(f"📊 Admin logged in: {request.session.get('admin_logged_in')}")
    print(f"📊 Admin email: {request.session.get('admin_email')}")
    print(f"📊 User authenticated: {hasattr(request, 'user') and request.user.is_authenticated}")
    if hasattr(request, 'user') and request.user.is_authenticated:
        print(f"📊 User ID: {request.user.id}")
        print(f"📊 User email: {request.user.email}")
        print(f"📊 User is superuser: {request.user.is_superuser}")
        print(f"📊 User is staff: {request.user.is_staff}")
    
    # Verificar se está logado como admin
    if not request.session.get('admin_logged_in'):
        print("❌ Sessão admin não encontrada, redirecionando para login")
        return redirect('/login/')
    
    print("✅ Sessão admin encontrada, verificando motoboy...")
    
    # Verificar se não é um motoboy (proteção adicional)
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            from motoboys.models import Motoboy
            motoboy = Motoboy.objects.get(user=request.user)
            print(f"⚠️ Usuário é motoboy: {motoboy.full_name}, redirecionando...")
            # Se for motoboy, redireciona para dashboard de motoboy
            return redirect('motoboys:dashboard')
        except Motoboy.DoesNotExist:
            print("✅ Usuário não é motoboy, continuando...")
            pass
    
    print("🎯 Renderizando admin dashboard...")
    return render(request, 'core/admin_dashboard.html')

def products_management(request):
    """Gerenciamento de produtos (CRUD)"""
    # Verificar se está logado como admin
    if not request.session.get('admin_logged_in'):
        return redirect('/login/')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'create':
                # Criar novo produto
                product = Product.objects.create(
                    name=data.get('name'),
                    description=data.get('description'),
                    price=float(data.get('price')),
                    category_id=data.get('category_id'),
                    is_available=data.get('is_available', True),
                    order=data.get('order', 0)
                )
                return JsonResponse({'success': True, 'message': 'Produto criado com sucesso!', 'product_id': product.id})
            
            elif action == 'update':
                # Atualizar produto existente
                product_id = data.get('product_id')
                product = Product.objects.get(id=product_id)
                product.name = data.get('name')
                product.description = data.get('description')
                product.price = float(data.get('price'))
                product.category_id = data.get('category_id')
                product.is_available = data.get('is_available', True)
                product.order = data.get('order', 0)
                product.save()
                return JsonResponse({'success': True, 'message': 'Produto atualizado com sucesso!'})
            
            elif action == 'delete':
                # Deletar produto
                product_id = data.get('product_id')
                Product.objects.filter(id=product_id).delete()
                return JsonResponse({'success': True, 'message': 'Produto deletado com sucesso!'})
            
            elif action == 'toggle_availability':
                # Alternar disponibilidade
                product_id = data.get('product_id')
                product = Product.objects.get(id=product_id)
                product.is_available = not product.is_available
                product.save()
                status = "disponível" if product.is_available else "indisponível"
                return JsonResponse({'success': True, 'message': f'Produto marcado como {status}!', 'is_available': product.is_available})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro: {str(e)}'})
    
    # GET: Listar produtos e categorias
    products = Product.objects.all().order_by('category__order', 'order', 'name')
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'core/products_management.html', context)

def logout(request):
    """Logout do sistema"""
    request.session.flush()
    return redirect('/login/')
