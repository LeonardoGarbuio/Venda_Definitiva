#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')
django.setup()

from motoboys.models import Motoboy
from users.models import User

print("=== DEBUG MOTOBOYS ===")

# Verificar todos os motoboys
motoboys = Motoboy.objects.all()
print(f"Total de motoboys: {motoboys.count()}")

for motoboy in motoboys:
    print(f"\nMotoboy: {motoboy.full_name}")
    print(f"  Email: {motoboy.user.email}")
    print(f"  Device IDs: {motoboy.device_ids}")
    print(f"  Criado em: {motoboy.created_at}")
    print(f"  Status: {motoboy.status}")

# Verificar usuários
users = User.objects.all()
print(f"\n=== USUÁRIOS ===")
print(f"Total de usuários: {users.count()}")

for user in users:
    print(f"  {user.email} - {user.username}")
