#!/usr/bin/env python
import os
import sys
import django
import requests
import json
import re

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from motoboys.models import Motoboy
from users.models import User

print("=== TESTE DE LOGIN ===")

# URL base
base_url = "http://127.0.0.1:8000"

# Dados de teste
test_email = "motoboy@teste.com"
test_password = "motoboy123"
test_device_id = "test_device_123"

print(f"Testando login com:")
print(f"  Email: {test_email}")
print(f"  Password: {test_password}")
print(f"  Device ID: {test_device_id}")

# Criar uma sessão para manter cookies
session = requests.Session()

try:
    # 1. Primeiro, acessar a página de login para obter o token CSRF
    print(f"\n1. Obtendo token CSRF...")
    login_page = session.get(f"{base_url}/motoboys/login/")
    
    if login_page.status_code != 200:
        print(f"❌ Erro ao acessar página de login: {login_page.status_code}")
        exit(1)
    
    # Extrair o token CSRF da página
    csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text)
    if not csrf_match:
        print("❌ Token CSRF não encontrado na página")
        exit(1)
    
    csrf_token = csrf_match.group(1)
    print(f"✅ Token CSRF obtido: {csrf_token[:20]}...")
    
    # 2. Fazer login com o token CSRF
    print(f"\n2. Fazendo login...")
    login_data = {
        "email": test_email,
        "password": test_password,
        "device_id": test_device_id,
        "remember_me": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
    }
    
    print(f"Dados enviados: {json.dumps(login_data, indent=2)}")
    
    response = session.post(
        f"{base_url}/motoboys/login/",
        json=login_data,
        headers=headers
    )
    
    print(f"Status da resposta: {response.status_code}")
    print(f"Resposta: {response.text}")
    
    if response.status_code == 200:
        print("✅ Login bem-sucedido!")
        
        # Verificar se o device_id foi salvo
        try:
            user = User.objects.get(email=test_email)
            motoboy = Motoboy.objects.get(user=user)
            
            print(f"\n=== VERIFICAÇÃO NO BANCO ===")
            print(f"Motoboy: {motoboy.full_name}")
            print(f"Device IDs antes: {motoboy.device_ids}")
            print(f"Tipo: {type(motoboy.device_ids)}")
            
            if test_device_id in (motoboy.device_ids or []):
                print("✅ Device ID foi salvo corretamente!")
            else:
                print("❌ Device ID NÃO foi salvo!")
                
        except Exception as e:
            print(f"❌ Erro ao verificar motoboy: {e}")
    else:
        print("❌ Login falhou!")
        
except Exception as e:
    print(f"❌ Erro na requisição: {e}")
    import traceback
    traceback.print_exc()

print("\n=== FIM DO TESTE ===")
