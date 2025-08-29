#!/usr/bin/env python
"""
Script para configurar o banco de dados no Render
Executa migrações e cria dados iniciais
"""
import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from django.core.management import execute_from_command_line
from core.models import Category, Product
from motoboys.models import Motoboy
from django.contrib.auth.models import User

def setup_render():
    print("🚀 === INICIANDO SETUP DO RENDER ===")
    
    try:
        # 1. Executa as migrações
        print("📋 Executando migrações...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrações executadas com sucesso!")
        
        # 2. Cria superusuário se não existir
        print("👑 Verificando superusuário...")
        if not User.objects.filter(is_superuser=True).exists():
            print("👑 Criando superusuário...")
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("✅ Superusuário criado!")
        else:
            print("✅ Superusuário já existe!")
        
        # 3. Cria categorias se não existirem
        print("🏷️ Verificando categorias...")
        categories_data = [
            'bebidas',
            'hamburgueres', 
            'acompanhamentos',
            'sobremesas',
            'bebidas_alcoolicas',
            'promocoes'
        ]
        
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'Categoria de {cat_name}'}
            )
            if created:
                print(f"✅ Categoria '{cat_name}' criada!")
            else:
                print(f"✅ Categoria '{cat_name}' já existe!")
        
        # 4. Cria produtos se não existirem
        print("🍔 Verificando produtos...")
        if not Product.objects.exists():
            print("🍔 Criando produtos de teste...")
            
            # Bebidas
            bebidas = Category.objects.get(name='bebidas')
            Product.objects.create(
                name='Coca-Cola 350ml',
                description='Refrigerante Coca-Cola 350ml',
                price=6.00,
                category=bebidas,
                is_available=True
            )
            Product.objects.create(
                name='Água 500ml',
                description='Água mineral 500ml',
                price=3.00,
                category=bebidas,
                is_available=True
            )
            
            # Hamburgueres
            hamburgueres = Category.objects.get(name='hamburgueres')
            Product.objects.create(
                name='Hambúrguer Clássico',
                description='Hambúrguer com carne, alface, tomate e queijo',
                price=18.00,
                category=hamburgueres,
                is_available=True
            )
            Product.objects.create(
                name='Hambúrguer Duplo',
                description='Hambúrguer duplo com bacon e queijo',
                price=24.00,
                category=hamburgueres,
                is_available=True
            )
            
            # Sobremesas
            sobremesas = Category.objects.get(name='sobremesas')
            Product.objects.create(
                name='Brigadeiro',
                description='Brigadeiro caseiro',
                price=4.00,
                category=sobremesas,
                is_available=True
            )
            
            print("✅ Produtos de teste criados!")
        else:
            print("✅ Produtos já existem!")
        
        # 5. Verifica motoboys
        print("🛵 Verificando motoboys...")
        if not Motoboy.objects.exists():
            print("🛵 Nenhum motoboy encontrado - sistema pronto para cadastros!")
        else:
            print(f"✅ {Motoboy.objects.count()} motoboys encontrados!")
        
        print("🎉 SETUP DO RENDER CONCLUÍDO COM SUCESSO!")
        print("🌐 Sistema pronto para uso!")
        
    except Exception as e:
        print(f"❌ ERRO NO SETUP: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_render()
