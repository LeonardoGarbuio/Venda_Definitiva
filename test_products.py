#!/usr/bin/env python
"""
Script para verificar se os produtos estão no banco
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from core.models import Category, Product

def test_products():
    """Verifica se os produtos estão no banco"""
    
    print("🔍 Verificando produtos no banco...")
    print("=" * 50)
    
    # 1. Verificar categorias
    print("📂 CATEGORIAS:")
    categories = Category.objects.all()
    for cat in categories:
        print(f"   ✅ {cat.name}: {cat.description}")
    
    print(f"\n📊 Total de categorias: {categories.count()}")
    
    # 2. Verificar produtos
    print("\n🛍️ PRODUTOS:")
    products = Product.objects.all()
    for prod in products:
        print(f"   ✅ {prod.name} - {prod.category.name} - R$ {prod.price}")
    
    print(f"\n📊 Total de produtos: {products.count()}")
    
    # 3. Verificar se estão disponíveis
    available_products = Product.objects.filter(is_available=True)
    print(f"📊 Produtos disponíveis: {available_products.count()}")
    
    print("=" * 50)
    
    if products.count() > 0:
        print("✅ Produtos encontrados no banco!")
    else:
        print("❌ Nenhum produto encontrado!")

if __name__ == "__main__":
    test_products()
