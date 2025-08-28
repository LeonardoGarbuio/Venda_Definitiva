from django.contrib import admin
from .models import Order, MenuItem, CartItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_available']
    ordering = ['category', 'name']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'session_key', 'quantity', 'total_price', 'added_at']
    list_filter = ['added_at', 'menu_item__category']
    search_fields = ['menu_item__name', 'session_key']
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin customizado para pedidos"""
    
    list_display = ('order_number', 'customer', 'status', 'priority', 'motoboy', 'final_price', 'created_at')
    list_filter = ('status', 'priority', 'is_fragile', 'created_at', 'delivered_at')
    search_fields = ('order_number', 'customer__first_name', 'customer__last_name', 'customer__email', 'pickup_address', 'delivery_address')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('order_number', 'customer', 'motoboy', 'status', 'priority')
        }),
        ('Endereços', {
            'fields': ('pickup_address', 'pickup_latitude', 'pickup_longitude', 'delivery_address', 'delivery_latitude', 'delivery_longitude')
        }),
        ('Detalhes da Entrega', {
            'fields': ('description', 'weight', 'dimensions', 'is_fragile')
        }),
        ('Valores e Distância', {
            'fields': ('base_price', 'distance_km', 'final_price')
        }),
        ('Avaliação', {
            'fields': ('rating', 'feedback'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'accepted_at', 'picked_up_at', 'delivered_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Tempos de Entrega', {
            'fields': ('estimated_delivery_time', 'actual_delivery_time'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'accepted_at', 'picked_up_at', 'delivered_at')
    
    list_editable = ('status', 'priority')
    
    actions = ['mark_as_accepted', 'mark_as_picked_up', 'mark_as_delivered', 'calculate_final_price']
    
    def mark_as_accepted(self, request, queryset):
        """Marca pedidos como aceitos"""
        updated = queryset.filter(status='pending').update(status='accepted')
        self.message_user(request, f'{updated} pedido(s) marcado(s) como aceito(s).')
    mark_as_accepted.short_description = "Marcar como aceito"
    
    def mark_as_picked_up(self, request, queryset):
        """Marca pedidos como retirados"""
        updated = queryset.filter(status='accepted').update(status='picked_up')
        self.message_user(request, f'{updated} pedido(s) marcado(s) como retirado(s).')
    mark_as_picked_up.short_description = "Marcar como retirado"
    
    def mark_as_delivered(self, request, queryset):
        """Marca pedidos como entregues"""
        updated = queryset.filter(status='picked_up').update(status='delivered')
        self.message_user(request, f'{updated} pedido(s) marcado(s) como entregue(s).')
    mark_as_delivered.short_description = "Marcar como entregue"
    
    def calculate_final_price(self, request, queryset):
        """Calcula preço final para pedidos selecionados"""
        updated = 0
        for order in queryset:
            if order.distance_km:
                order.calculate_final_price()
                updated += 1
        self.message_user(request, f'Preço final calculado para {updated} pedido(s).')
    calculate_final_price.short_description = "Calcular preço final"
    
    def get_queryset(self, request):
        """Filtra apenas pedidos"""
        return super().get_queryset(request)
    
    def has_delete_permission(self, request, obj=None):
        """Permite deletar pedidos"""
        return True
    
    def has_change_permission(self, request, obj=None):
        """Permite editar pedidos"""
        return True
    
    def get_readonly_fields(self, request, obj=None):
        """Campos somente leitura baseados no status"""
        if obj and obj.status in ['delivered', 'cancelled', 'failed']:
            return self.readonly_fields + ('status', 'motoboy')
        return self.readonly_fields
