#!/usr/bin/env python
"""
Script para resetar todos os device_ids dos motoboys
"""

import os
import sys
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from motoboys.models import Motoboy

def reset_device_ids():
    """Reseta todos os device_ids para lista vazia"""
    
    print("🧹 === RESETANDO DEVICE_IDS ===")
    
    # Busca todos os motoboys
    motoboys = Motoboy.objects.all()
    total = motoboys.count()
    
    print(f"📊 Total de motoboys encontrados: {total}")
    
    if total == 0:
        print("❌ Nenhum motoboy encontrado no banco")
        return
    
    # Confirma a ação
    print("\n⚠️  ATENÇÃO: Isso vai limpar TODOS os device_ids!")
    confirm = input("Digite 'SIM' para confirmar: ")
    
    if confirm != 'SIM':
        print("❌ Operação cancelada")
        return
    
    # Limpa os device_ids
    updated = 0
    for motoboy in motoboys:
        if motoboy.device_ids:  # Se tem device_ids
            print(f"🧹 Limpando device_ids de: {motoboy.full_name}")
            print(f"   Antes: {motoboy.device_ids}")
            
            motoboy.device_ids = []  # Lista vazia
            motoboy.save()
            
            print(f"   Depois: {motoboy.device_ids}")
            updated += 1
        else:
            print(f"✅ {motoboy.full_name} já está limpo")
    
    print(f"\n🎉 RESET CONCLUÍDO!")
    print(f"📊 Motoboys atualizados: {updated}")
    print(f"📊 Total no banco: {total}")
    
    # Verifica o resultado
    print(f"\n🔍 VERIFICANDO RESULTADO...")
    for motoboy in Motoboy.objects.all():
        print(f"  📋 {motoboy.full_name}: {motoboy.device_ids}")

if __name__ == '__main__':
    reset_device_ids()
