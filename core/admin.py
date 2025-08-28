from django.contrib import admin
from .models import DeliveryStatistics, MotoboyPerformance

@admin.register(DeliveryStatistics)
class DeliveryStatisticsAdmin(admin.ModelAdmin):
    """Admin para estatísticas de entregas"""
    
    list_display = ('date', 'total_orders', 'completed_orders', 'total_revenue', 'average_rating', 'active_motoboys')
    list_filter = ('date',)
    ordering = ('-date',)
    
    fieldsets = (
        ('Data', {
            'fields': ('date',)
        }),
        ('Contadores', {
            'fields': ('total_orders', 'completed_orders', 'cancelled_orders', 'failed_orders')
        }),
        ('Valores', {
            'fields': ('total_revenue', 'average_delivery_time')
        }),
        ('Motoboys', {
            'fields': ('active_motoboys', 'total_motoboys')
        }),
        ('Qualidade', {
            'fields': ('average_rating', 'customer_satisfaction')
        }),
        ('Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['generate_today_stats', 'generate_week_stats']
    
    def generate_today_stats(self, request, queryset):
        """Gera estatísticas para hoje"""
        from django.utils import timezone
        stats = DeliveryStatistics.generate_daily_stats()
        self.message_user(request, f'Estatísticas geradas para {stats.date}.')
    generate_today_stats.short_description = "Gerar estatísticas de hoje"
    
    def generate_week_stats(self, request, queryset):
        """Gera estatísticas para a semana atual"""
        from django.utils import timezone
        from datetime import timedelta
        
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        
        for i in range(7):
            date = start_of_week + timedelta(days=i)
            DeliveryStatistics.generate_daily_stats(date)
        
        self.message_user(request, 'Estatísticas da semana geradas com sucesso.')
    generate_week_stats.short_description = "Gerar estatísticas da semana"
    
    def has_add_permission(self, request):
        """Não permite adicionar manualmente"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Permite deletar estatísticas"""
        return True
    
    def has_change_permission(self, request, obj=None):
        """Permite editar estatísticas"""
        return True

@admin.register(MotoboyPerformance)
class MotoboyPerformanceAdmin(admin.ModelAdmin):
    """Admin para performance dos motoboys"""
    
    list_display = ('motoboy', 'month', 'year', 'total_deliveries', 'successful_deliveries', 'average_rating', 'total_earnings')
    list_filter = ('month', 'year', 'motoboy__is_active')
    search_fields = ('motoboy__full_name', 'motoboy__vehicle_plate')
    ordering = ('-year', '-month')
    
    fieldsets = (
        ('Identificação', {
            'fields': ('motoboy', 'month', 'year')
        }),
        ('Métricas de Performance', {
            'fields': ('total_deliveries', 'successful_deliveries', 'failed_deliveries')
        }),
        ('Tempo e Distância', {
            'fields': ('total_distance', 'average_delivery_time')
        }),
        ('Avaliações e Ganhos', {
            'fields': ('average_rating', 'total_earnings')
        }),
        ('Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['generate_current_month_stats', 'generate_last_month_stats']
    
    def generate_current_month_stats(self, request, queryset):
        """Gera estatísticas para o mês atual"""
        from django.utils import timezone
        
        now = timezone.now()
        month = now.month
        year = now.year
        
        from motoboys.models import Motoboy
        motoboys = Motoboy.objects.filter(is_active=True)
        
        for motoboy in motoboys:
            MotoboyPerformance.generate_monthly_stats(motoboy, month, year)
        
        self.message_user(request, f'Estatísticas do mês {month}/{year} geradas com sucesso.')
    generate_current_month_stats.short_description = "Gerar estatísticas do mês atual"
    
    def generate_last_month_stats(self, request, queryset):
        """Gera estatísticas para o mês anterior"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        last_month = now - timedelta(days=30)
        month = last_month.month
        year = last_month.year
        
        from motoboys.models import Motoboy
        motoboys = Motoboy.objects.filter(is_active=True)
        
        for motoboy in motoboys:
            MotoboyPerformance.generate_monthly_stats(motoboy, month, year)
        
        self.message_user(request, f'Estatísticas do mês {month}/{year} geradas com sucesso.')
    generate_last_month_stats.short_description = "Gerar estatísticas do mês anterior"
    
    def has_add_permission(self, request):
        """Não permite adicionar manualmente"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Permite deletar performance"""
        return True
    
    def has_change_permission(self, request, obj=None):
        """Permite editar performance"""
        return True
