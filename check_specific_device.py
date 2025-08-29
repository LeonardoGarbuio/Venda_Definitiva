#!/usr/bin/env python
import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from motoboys.models import Motoboy

def check_specific_device():
    target_device_id = "290b89208ec2da38"
    
    print(f"🔍 VERIFICANDO DEVICE_ID ESPECÍFICO: {target_device_id}")
    print(f"🔍 Tamanho: {len(target_device_id)}")
    
    # Verifica todos os motoboys
    motoboys = Motoboy.objects.all()
    print(f"📊 Total de motoboys: {motoboys.count()}")
    
    found = False
    for i, motoboy in enumerate(motoboys):
        print(f"\n📋 MOTOBOY {i+1}: {motoboy.full_name}")
        print(f"   Email: {motoboy.user.email}")
        print(f"   Device IDs: {motoboy.device_ids}")
        
        if motoboy.device_ids:
            for device_id in motoboy.device_ids:
                print(f"   🔍 Verificando: '{device_id}' vs '{target_device_id}'")
                print(f"   🔍 São iguais? {device_id == target_device_id}")
                print(f"   🔍 Tamanhos: {len(device_id)} vs {len(target_device_id)}")
                
                if device_id == target_device_id:
                    found = True
                    print(f"   🎯 MATCH ENCONTRADO!")
                    print(f"   ✅ Este motoboy já tem este device_id!")
                    return motoboy
    
    if not found:
        print(f"\n❌ DEVICE_ID '{target_device_id}' NÃO ENCONTRADO NO BANCO!")
        print(f"❌ Por isso o backend está retornando 'show_register: true'")
        print(f"❌ O sistema está funcionando como esperado para um dispositivo novo")
    
    return None

if __name__ == "__main__":
    result = check_specific_device()
    if result:
        print(f"\n✅ RESULTADO: Motoboy encontrado - {result.full_name}")
    else:
        print(f"\n❌ RESULTADO: Nenhum motoboy com este device_id")
