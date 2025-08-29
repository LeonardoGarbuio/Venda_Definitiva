#!/usr/bin/env python
import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from motoboys.models import Motoboy

def test_device_id_sync():
    print("🔍 TESTANDO SINCRONIZAÇÃO DO DEVICE_ID...")
    
    # Verifica todos os motoboys e seus device_ids
    motoboys = Motoboy.objects.all()
    print(f"📊 Total de motoboys: {motoboys.count()}")
    
    print("\n📋 DEVICE_IDS NO BANCO:")
    for i, motoboy in enumerate(motoboys):
        print(f"  {i+1}. {motoboy.full_name} ({motoboy.user.email})")
        if motoboy.device_ids:
            for device_id in motoboy.device_ids:
                print(f"     Device ID: {device_id} (tamanho: {len(device_id)})")
        else:
            print(f"     SEM DEVICE_IDS!")
    
    print("\n🔍 PROBLEMA IDENTIFICADO:")
    print("  - Frontend está enviando: device_ids de 8 caracteres (ex: 50ed5d3f)")
    print("  - Backend tem salvos: device_ids de 16 caracteres (ex: 290b89208ec2da38)")
    print("  - São IDs COMPLETAMENTE DIFERENTES!")
    
    print("\n🎯 SOLUÇÃO:")
    print("  - Frontend e backend precisam usar a MESMA lógica de geração")
    print("  - Ou o frontend precisa usar o device_id que o backend gera")

if __name__ == "__main__":
    test_device_id_sync()
