#!/usr/bin/env python
"""
Script para criar produtos de teste no banco de dados
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from core.models import Category, Product

def create_test_products():
    """Cria produtos de teste para o sistema funcionar"""
    
    print("🛍️ Criando produtos de teste...")
    
    # 1. Criar categorias
    print("1️⃣ Criando categorias...")
    
    categories = {
        'burgers': '🍔 Hambúrgueres artesanais e especiais',
        'pizzas': '🍕 Pizzas tradicionais e especiais',
        'drinks': '🥤 Refrigerantes, sucos e água',
        'desserts': '🍰 Doces e sobremesas',
        'salads': '🥗 Saladas frescas e saudáveis'
    }
    
    created_categories = {}
    for name, description in categories.items():
        category, created = Category.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        if created:
            print(f"   ✅ Categoria criada: {name}")
        else:
            print(f"   ℹ️  Categoria já existe: {name}")
        created_categories[name] = category
    
    # 2. Criar produtos
    print("\n2️⃣ Criando produtos...")
    
    products_data = [
        # Hambúrgueres (burgers)
        {
            'name': 'Hambúrguer Clássico',
            'category': 'burgers',
            'description': 'Carne, alface, tomate, cebola e queijo',
            'price': 18.90,
            'image': 'burger-classico.jpg'
        },
        {
            'name': 'Hambúrguer Duplo',
            'category': 'burgers',
            'description': 'Duas carnes, queijo, bacon e molho especial',
            'price': 24.90,
            'image': 'burger-duplo.jpg'
        },
        {
            'name': 'Hambúrguer Vegetariano',
            'category': 'burgers',
            'description': 'Hambúrguer de grão-de-bico com vegetais',
            'price': 22.90,
            'image': 'burger-vegetariano.jpg'
        },
        
        # Pizzas (pizzas)
        {
            'name': 'Pizza Margherita',
            'category': 'pizzas',
            'description': 'Molho de tomate, mussarela e manjericão',
            'price': 25.90,
            'image': 'pizza-margherita.jpg'
        },
        {
            'name': 'Pizza Pepperoni',
            'category': 'pizzas',
            'description': 'Molho de tomate, mussarela e pepperoni',
            'price': 28.90,
            'image': 'pizza-pepperoni.jpg'
        },
        {
            'name': 'Pizza Quatro Queijos',
            'category': 'pizzas',
            'description': 'Molho de tomate e quatro tipos de queijo',
            'price': 32.90,
            'image': 'pizza-quatro-queijos.jpg'
        },
        {
            'name': 'Pizza Calabresa',
            'category': 'pizzas',
            'description': 'Molho de tomate, mussarela e calabresa',
            'price': 26.90,
            'image': 'pizza-calabresa.jpg'
        },
        
        # Bebidas (drinks)
        {
            'name': 'Coca-Cola 350ml',
            'category': 'drinks',
            'description': 'Refrigerante Coca-Cola',
            'price': 6.90,
            'image': 'coca-cola.jpg'
        },
        {
            'name': 'Água Mineral 500ml',
            'category': 'drinks',
            'description': 'Água mineral natural',
            'price': 3.90,
            'image': 'agua.jpg'
        },
        {
            'name': 'Suco de Laranja 300ml',
            'category': 'drinks',
            'description': 'Suco natural de laranja',
            'price': 8.90,
            'image': 'suco-laranja.jpg'
        },
        {
            'name': 'Guaraná 350ml',
            'category': 'drinks',
            'description': 'Refrigerante Guaraná',
            'price': 6.90,
            'image': 'guarana.jpg'
        },
        
        # Sobremesas (desserts)
        {
            'name': 'Pudim de Leite',
            'category': 'desserts',
            'description': 'Pudim tradicional de leite condensado',
            'price': 12.90,
            'image': 'pudim.jpg'
        },
        {
            'name': 'Brigadeiro',
            'category': 'desserts',
            'description': 'Brigadeiro caseiro',
            'price': 4.90,
            'image': 'brigadeiro.jpg'
        },
        {
            'name': 'Sorvete de Chocolate',
            'category': 'desserts',
            'description': 'Sorvete cremoso de chocolate',
            'price': 15.90,
            'image': 'sorvete-chocolate.jpg'
        },
        
        # Saladas (salads)
        {
            'name': 'Salada Caesar',
            'category': 'salads',
            'description': 'Alface, croutons, parmesão e molho caesar',
            'price': 18.90,
            'image': 'salada-caesar.jpg'
        },
        {
            'name': 'Salada Tropical',
            'category': 'salads',
            'description': 'Mix de folhas, manga, abacaxi e granola',
            'price': 22.90,
            'image': 'salada-tropical.jpg'
        }
    ]
    
    for product_data in products_data:
        category = created_categories[product_data['category']]
        
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': category,
                'description': product_data['description'],
                'price': product_data['price'],
                'image': product_data['image'],
                'is_available': True
            }
        )
        
        if created:
            print(f"   ✅ Produto criado: {product_data['name']} - R$ {product_data['price']}")
        else:
            print(f"   ℹ️  Produto já existe: {product_data['name']}")
    
    # 3. Verificar
    print("\n🔍 Verificando produtos criados...")
    
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    
    print(f"   📊 Total de categorias: {total_categories}")
    print(f"   📊 Total de produtos: {total_products}")
    
    if total_products > 0:
        print("\n✅ Produtos criados com sucesso!")
        print("🛒 Agora o sistema de pedidos deve funcionar!")
    else:
        print("\n❌ Nenhum produto foi criado!")
    
    print("=" * 50)

if __name__ == "__main__":
    create_test_products()
