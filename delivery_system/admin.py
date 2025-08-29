from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

# Configuração personalizada do admin
class MotoDeliveryAdminSite(AdminSite):
    site_header = _('MotoDelivery Admin')
    site_title = _('MotoDelivery Admin Portal')
    index_title = _('Bem-vindo ao Portal Administrativo')
    
    # Desabilita o sistema de motoboy no admin
    def has_permission(self, request):
        # Se for admin, permite acesso
        if request.user.is_superuser:
            return True
        # Se for staff, permite acesso
        if request.user.is_staff:
            return True
        return False

# Instância personalizada do admin
admin_site = MotoDeliveryAdminSite(name='motodelivery_admin')

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
