from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin customizado para usuários"""
    
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'city', 'state', 'is_active', 'created_at')
    list_filter = ('is_active', 'city', 'state', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'address', 'city')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        ('Endereço', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Localização', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Datas importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'zip_code', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    
    def get_queryset(self, request):
        """Filtra apenas usuários que não são staff"""
        return super().get_queryset(request).filter(is_staff=False)
    
    def has_delete_permission(self, request, obj=None):
        """Permite deletar usuários"""
        return True
    
    def has_change_permission(self, request, obj=None):
        """Permite editar usuários"""
        return True
