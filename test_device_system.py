#!/usr/bin/env python
"""
Script para testar o sistema de device_id
"""
import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from motoboys.models import Motoboy
from motoboys.views import generate_device_id, check_existing_device_registration
from django.test import RequestFactory

def test_device_system():
    print("🧪 === TESTE DO SISTEMA DE DEVICE_ID ===")
    
    # 1. Verifica motoboys existentes
    print("\n1️⃣ MOTOBOYS EXISTENTES:")
    motoboys = Motoboy.objects.all()
    print(f"   Total: {motoboys.count()}")
    
    for i, moto in enumerate(motoboys, 1):
        print(f"   {i}. {moto.full_name}")
        print(f"      Email: {moto.user.email}")
        print(f"      Device IDs: {moto.device_ids}")
        print()
    
    # 2. Testa geração de device_id
    print("2️⃣ TESTANDO GERAÇÃO DE DEVICE_ID:")
    factory = RequestFactory()
    request = factory.get('/')
    request.META['HTTP_USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    request.META['HTTP_ACCEPT_LANGUAGE'] = 'pt-BR,pt;q=0.9,en;q=0.8'
    request.META['HTTP_ACCEPT_ENCODING'] = 'gzip, deflate, br'
    request.META['HTTP_HOST'] = '127.0.0.1:8000'
    request.META['REMOTE_ADDR'] = '127.0.0.1'
    
    device_id = generate_device_id(request)
    print(f"   Device ID gerado: {device_id}")
    
    # 3. Testa verificação de device_id existente
    print("\n3️⃣ TESTANDO VERIFICAÇÃO DE DEVICE_ID:")
    existing_motoboy = check_existing_device_registration(device_id, request)
    
    if existing_motoboy:
        print(f"   ✅ ENCONTROU: {existing_motoboy.full_name}")
    else:
        print(f"   ❌ NÃO ENCONTROU - dispositivo novo")
    
    # 4. Testa com device_id conhecido
    print("\n4️⃣ TESTANDO COM DEVICE_ID CONHECIDO:")
    if motoboys.exists():
        moto = motoboys.first()
        if moto.device_ids:
            known_device_id = moto.device_ids[0]
            print(f"   Testando com: {known_device_id}")
            existing = check_existing_device_registration(known_device_id, request)
            if existing:
                print(f"   ✅ ENCONTROU: {existing.full_name}")
            else:
                print(f"   ❌ NÃO ENCONTROU (problema!)")
        else:
            print(f"   ⚠️ Motoboy {moto.full_name} não tem device_ids")
    
    print("\n🧪 === FIM DO TESTE ===")

if __name__ == "__main__":
    test_device_system()
