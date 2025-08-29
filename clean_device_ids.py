#!/usr/bin/env python
"""
Script para limpar device_ids fixos do banco de dados
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from motoboys.models import Motoboy

def clean_device_ids():
    """Limpa todos os device_ids fixos do banco"""
    
    print("🧹 Limpando device_ids fixos do banco...")
    
    # Busca todos os motoboys
    motoboys = Motoboy.objects.all()
    
    for motoboy in motoboys:
        print(f"Motoboy: {motoboy.full_name}")
        print(f"  Device IDs antes: {motoboy.device_ids}")
        
        # Limpa os device_ids
        motoboy.device_ids = []
        motoboy.save()
        
        print(f"  Device IDs depois: {motoboy.device_ids}")
        print("---")
    
    print("✅ Device IDs limpos com sucesso!")
    print("🔄 Agora o sistema vai gerar IDs únicos automaticamente")

if __name__ == "__main__":
    clean_device_ids()
