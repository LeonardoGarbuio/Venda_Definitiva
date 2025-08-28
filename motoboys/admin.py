from django.contrib import admin
from .models import Motoboy

@admin.register(Motoboy)
class MotoboyAdmin(admin.ModelAdmin):
    """Admin customizado para motoboys"""
    
    list_display = ('full_name', 'phone_number', 'vehicle_plate', 'status', 'rating', 'total_deliveries', 'is_active', 'created_at')
    list_filter = ('status', 'is_active', 'vehicle_year', 'created_at')
    search_fields = ('full_name', 'phone_number', 'document_number', 'vehicle_plate', 'vehicle_model')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Identificação', {
            'fields': ('user', 'full_name', 'phone_number')
        }),
        ('Documentos', {
            'fields': ('document_type', 'document_number')
        }),
        ('Veículo', {
            'fields': ('vehicle_model', 'vehicle_plate', 'vehicle_year', 'vehicle_color')
        }),
        ('Localização Atual', {
            'fields': ('current_latitude', 'current_longitude', 'last_location_update'),
            'classes': ('collapse',)
        }),
        ('Status e Performance', {
            'fields': ('status', 'is_active', 'rating', 'total_deliveries', 'successful_deliveries')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_location_update', 'total_deliveries', 'successful_deliveries')
    
    list_editable = ('status', 'is_active')
    
    actions = ['activate_motoboys', 'deactivate_motoboys', 'set_available', 'set_offline']
    
    def activate_motoboys(self, request, queryset):
        """Ativa motoboys selecionados"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} motoboy(s) ativado(s) com sucesso.')
    activate_motoboys.short_description = "Ativar motoboys selecionados"
    
    def deactivate_motoboys(self, request, queryset):
        """Desativa motoboys selecionados"""
        updated = queryset.update(is_active=False, status='offline')
        self.message_user(request, f'{updated} motoboy(s) desativado(s) com sucesso.')
    deactivate_motoboys.short_description = "Desativar motoboys selecionados"
    
    def set_available(self, request, queryset):
        """Define motoboys como disponíveis"""
        updated = queryset.update(status='available')
        self.message_user(request, f'{updated} motoboy(s) definido(s) como disponível(is).')
    set_available.short_description = "Definir como disponível"
    
    def set_offline(self, request, queryset):
        """Define motoboys como offline"""
        updated = queryset.update(status='offline')
        self.message_user(request, f'{updated} motoboy(s) definido(s) como offline.')
    set_offline.short_description = "Definir como offline"
    
    def get_queryset(self, request):
        """Filtra apenas motoboys"""
        return super().get_queryset(request)
    
    def has_delete_permission(self, request, obj=None):
        """Permite deletar motoboys"""
        return True
    
    def has_change_permission(self, request, obj=None):
        """Permite editar motoboys"""
        return True
