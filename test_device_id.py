#!/usr/bin/env python
import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from motoboys.models import Motoboy

def test_device_id():
    print("🔍 TESTANDO DEVICE_ID...")
    
    # Simula a string que o frontend está enviando
    device_id_frontend = "589f86e0"
    
    print(f"Device ID do frontend: {device_id_frontend}")
    
    # Verifica se existe no banco
    motoboys = Motoboy.objects.all()
    print(f"Total de motoboys: {motoboys.count()}")
    
    found = False
    for motoboy in motoboys:
        if motoboy.device_ids and device_id_frontend in motoboy.device_ids:
            print(f"✅ ENCONTROU! Motoboy: {motoboy.full_name}")
            found = True
            break
    
    if not found:
        print("❌ Device ID não encontrado no banco!")
        print("\n📋 Device IDs existentes no banco:")
        for motoboy in motoboys:
            print(f"  {motoboy.full_name}: {motoboy.device_ids}")
    
    # Agora vamos ver se conseguimos fazer login com um motoboy existente
    print(f"\n🔍 TESTANDO LOGIN COM MOTOBOY EXISTENTE...")
    
    # Pega o primeiro motoboy
    if motoboys.exists():
        motoboy = motoboys.first()
        print(f"Tentando login com: {motoboy.full_name}")
        print(f"Email: {motoboy.user.email}")
        print(f"Device IDs: {motoboy.device_ids}")
        
        # Simula o que deveria acontecer
        if motoboy.device_ids:
            print(f"✅ Este motoboy deveria aparecer como 'Login' para os device_ids: {motoboy.device_ids}")
        else:
            print(f"⚠️ Este motoboy não tem device_ids configurados")

if __name__ == "__main__":
    test_device_id()
