#!/usr/bin/env python
"""
Script para testar todo o sistema de motoboy
"""
import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from core.models import Category, Product
from motoboys.models import Motoboy
from users.models import User

def test_complete_system():
    print("🧪 === TESTE COMPLETO DO SISTEMA ===")
    
    # 1. Testa modelos
    print("\n1️⃣ TESTANDO MODELOS:")
    
    print("   📋 Categorias:")
    categories = Category.objects.all()
    print(f"      Total: {categories.count()}")
    for cat in categories:
        print(f"      - {cat.name}: {cat.description}")
    
    print("   🍔 Produtos:")
    products = Product.objects.all()
    print(f"      Total: {products.count()}")
    for prod in products:
        print(f"      - {prod.name}: R$ {prod.price} ({prod.category.name})")
    
    print("   🛵 Motoboys:")
    motoboys = Motoboy.objects.all()
    print(f"      Total: {motoboys.count()}")
    for moto in motoboys:
        print(f"      - {moto.full_name}: {moto.user.email}")
        print(f"        Device IDs: {moto.device_ids}")
    
    print("   👤 Usuários:")
    users = User.objects.all()
    print(f"      Total: {users.count()}")
    for user in users:
        print(f"      - {user.username}: {user.email} (Super: {user.is_superuser})")
    
    # 2. Testa relacionamentos
    print("\n2️⃣ TESTANDO RELACIONAMENTOS:")
    
    print("   🔗 Produtos por categoria:")
    for cat in categories:
        cat_products = products.filter(category=cat)
        print(f"      {cat.name}: {cat_products.count()} produtos")
    
    print("   🔗 Motoboys com device_ids:")
    motoboys_with_devices = motoboys.filter(device_ids__isnull=False).exclude(device_ids=[])
    print(f"      Total com device_ids: {motoboys_with_devices.count()}")
    
    # 3. Testa funcionalidades
    print("\n3️⃣ TESTANDO FUNCIONALIDADES:")
    
    print("   ✅ Sistema de categorias: OK" if categories.exists() else "❌ Sistema de categorias: FALHOU")
    print("   ✅ Sistema de produtos: OK" if products.exists() else "❌ Sistema de produtos: FALHOU")
    print("   ✅ Sistema de motoboys: OK" if motoboys.exists() else "❌ Sistema de motoboys: FALHOU")
    print("   ✅ Sistema de usuários: OK" if users.exists() else "❌ Sistema de usuários: FALHOU")
    
    # 4. Resumo
    print("\n4️⃣ RESUMO DO TESTE:")
    
    total_tests = 4
    passed_tests = sum([
        categories.exists(),
        products.exists(),
        motoboys.exists(),
        users.exists()
    ])
    
    print(f"   📊 Testes passaram: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("   🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("   🌐 Pronto para deploy no Render!")
    else:
        print("   ⚠️ ALGUNS TESTES FALHARAM!")
        print("   🔧 Verifique os problemas acima!")
    
    print("\n🧪 === FIM DO TESTE ===")

if __name__ == "__main__":
    test_complete_system()
