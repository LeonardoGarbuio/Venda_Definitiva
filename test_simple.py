#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from motoboys.models import Motoboy
from users.models import User

print("=== TESTE SIMPLES ===")

# Verificar se o motoboy existe
try:
    user = User.objects.get(email="motoboy@teste.com")
    motoboy = Motoboy.objects.get(user=user)
    
    print(f"Motoboy encontrado: {motoboy.full_name}")
    print(f"Device IDs atuais: {motoboy.device_ids}")
    print(f"Tipo: {type(motoboy.device_ids)}")
    
    # Testar adicionar device_id
    test_device_id = "test_device_123"
    
    if not motoboy.device_ids:
        motoboy.device_ids = []
    
    if test_device_id not in motoboy.device_ids:
        motoboy.device_ids.append(test_device_id)
        motoboy.save()
        print(f"✅ Device ID adicionado: {test_device_id}")
        print(f"✅ Device IDs finais: {motoboy.device_ids}")
    else:
        print(f"⚠️ Device ID já existe: {test_device_id}")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("=== FIM DO TESTE ===")
