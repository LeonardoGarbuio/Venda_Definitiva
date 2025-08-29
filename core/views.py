from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            # Credenciais fixas que você pode alterar
            ADMIN_EMAIL = 'admin@motodelivery.com'
            ADMIN_PASSWORD = 'admin123'
            
            # Verificar credenciais
            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                # Criar sessão
                request.session['admin_logged_in'] = True
                request.session['admin_email'] = email
                return JsonResponse({'success': True, 'redirect': '/admin_dashboard/'})
            else:
                return JsonResponse({'success': False, 'message': 'Email ou senha incorretos.'})
        except:
            return JsonResponse({'success': False, 'message': 'Erro no servidor.'})
    
    return render(request, 'core/login.html')

def admin_dashboard(request):
    """Dashboard administrativo"""
    # Verificar se está logado
    if not request.session.get('admin_logged_in'):
        return redirect('/login/')
    return render(request, 'core/admin_dashboard.html')

def logout(request):
    """Logout do sistema"""
    request.session.flush()
    return redirect('/login/')
