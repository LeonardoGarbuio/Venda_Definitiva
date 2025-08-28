from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User

# Configurações do admin
admin.site.site_header = "Sistema de Delivery - Administração"
admin.site.site_title = "Admin Delivery"
admin.site.index_title = "Bem-vindo ao Sistema de Delivery"

# Remove o modelo User padrão do Django e registra o customizado
admin.site.unregister(Group)

# Personaliza o admin do usuário customizado
class CustomUserAdmin(BaseUserAdmin):
    """Admin customizado para o usuário customizado"""
    pass

# Registra o usuário customizado
admin.site.register(User, CustomUserAdmin)
