#!/usr/bin/env python
"""
Script para testar o login de motoboy e identificar erros
"""

import os
import sys
import django
import json

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import authenticate
from motoboys.views import motoboy_login
from motoboys.models import Motoboy
from django.contrib.auth.models import User

def test_login():
    """Testa o login de motoboy"""
    
    print("🧪 === TESTE DE LOGIN MOTOBOY ===")
    
    # Cria uma requisição fake com middleware de sessão
    factory = RequestFactory()
    
    # Dados de teste
    test_data = {
        'email': 'sasor111i@gmail.com',  # Email que existe no banco
        'password': '202330',  # Senha que sabemos
        'device_id': '6a70d4cb',
        'remember_me': False
    }
    
    print(f"📧 Email: {test_data['email']}")
    print(f"🔑 Password: {test_data['password']}")
    print(f"📱 Device ID: {test_data['device_id']}")
    
    # Testa autenticação direta
    print("\n🔍 Testando autenticação direta...")
    user = authenticate(username=test_data['email'], password=test_data['password'])
    
    if user:
        print(f"✅ Usuário autenticado: {user.username}")
        
        # Verifica se é motoboy
        try:
            motoboy = Motoboy.objects.get(user=user)
            print(f"✅ Motoboy encontrado: {motoboy.full_name}")
            print(f"📱 Device IDs atuais: {motoboy.device_ids}")
            
            # Testa adicionar device_id
            print(f"\n🔧 Testando adicionar device_id...")
            current_device_ids = motoboy.device_ids or []
            print(f"Lista atual: {current_device_ids}")
            
            if test_data['device_id'] not in current_device_ids:
                current_device_ids.append(test_data['device_id'])
                motoboy.device_ids = current_device_ids
                motoboy.save()
                print(f"✅ Device ID adicionado com sucesso!")
                print(f"📱 Nova lista: {motoboy.device_ids}")
            else:
                print(f"⚠️ Device ID já existe")
                
        except Motoboy.DoesNotExist:
            print(f"❌ Usuário não é motoboy")
    else:
        print(f"❌ Falha na autenticação")
    
    # Testa a view de login
    print(f"\n🌐 Testando view de login...")
    request = factory.post('/motoboys/login/', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    # Adiciona middleware de sessão
    from django.contrib.sessions.middleware import SessionMiddleware
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    
    try:
        response = motoboy_login(request)
        print(f"✅ Response status: {response.status_code}")
        if hasattr(response, 'content'):
            print(f"📄 Response content: {response.content.decode()}")
    except Exception as e:
        print(f"❌ Erro na view: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🏁 === FIM DO TESTE ===")

if __name__ == '__main__':
    test_login()
