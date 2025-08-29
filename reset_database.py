#!/usr/bin/env python
"""
Script para resetar completamente o banco de dados
CUIDADO: Isso vai apagar TODOS os dados!
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from django.db import connection

def reset_database():
    """Reseta completamente o banco de dados"""
    
    print("🗑️ RESETANDO BANCO DE DADOS COMPLETAMENTE...")
    print("⚠️  ATENÇÃO: Todos os dados serão perdidos!")
    print("=" * 50)
    
    # 1. Limpar todas as tabelas usando SQL direto
    print("1️⃣ Limpando todas as tabelas...")
    
    with connection.cursor() as cursor:
        # Lista de tabelas para limpar (apenas as que existem)
        tables = [
            'orders_order', 
            'motoboys_motoboy'
        ]
        
        for table in tables:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"   ✅ Tabela {table} limpa")
            except Exception as e:
                print(f"   ⚠️  Tabela {table}: {e}")
    
    # 2. Verificar se está limpo
    print("\n🔍 Verificando se o banco está limpo...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM motoboys_motoboy")
            motoboy_count = cursor.fetchone()[0]
            print(f"   📊 Motoboys: {motoboy_count}")
            
            cursor.execute("SELECT COUNT(*) FROM orders_order")
            order_count = cursor.fetchone()[0]
            print(f"   📊 Pedidos: {order_count}")
    except Exception as e:
        print(f"   📊 Erro ao verificar: {e}")
        motoboy_count = 0
        order_count = 0
    
    if motoboy_count == 0 and order_count == 0:
        print("\n✅ BANCO DE DADOS COMPLETAMENTE LIMPO!")
        print("🔄 Agora você pode começar do zero!")
    else:
        print("\n❌ Algumas tabelas ainda têm dados!")
    
    print("=" * 50)

if __name__ == "__main__":
    # Confirmação de segurança
    print("⚠️  ATENÇÃO: Este script vai APAGAR TODOS os dados do banco!")
    print("⚠️  Não há como desfazer esta ação!")
    
    confirm = input("Digite 'RESET' para confirmar: ")
    
    if confirm == "RESET":
        reset_database()
    else:
        print("❌ Operação cancelada!")
