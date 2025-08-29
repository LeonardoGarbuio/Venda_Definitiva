from django.db import models
from django.conf import settings
from motoboys.models import Motoboy
from orders.models import Order
from django.utils import timezone
from datetime import datetime, timedelta

class DeliveryStatistics(models.Model):
    """Modelo para estatísticas de entregas"""
    
    date = models.DateField(unique=True, verbose_name="Data")
    
    # Contadores
    total_orders = models.PositiveIntegerField(default=0, verbose_name="Total de pedidos")
    completed_orders = models.PositiveIntegerField(default=0, verbose_name="Pedidos completados")
    cancelled_orders = models.PositiveIntegerField(default=0, verbose_name="Pedidos cancelados")
    failed_orders = models.PositiveIntegerField(default=0, verbose_name="Pedidos que falharam")
    
    # Valores
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Receita total")
    average_delivery_time = models.PositiveIntegerField(default=0, verbose_name="Tempo médio de entrega (minutos)")
    
    # Motoboys
    active_motoboys = models.PositiveIntegerField(default=0, verbose_name="Motoboys ativos")
    total_motoboys = models.PositiveIntegerField(default=0, verbose_name="Total de motoboys")
    
    # Métricas de qualidade
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Avaliação média")
    customer_satisfaction = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Satisfação do cliente (%)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    class Meta:
        verbose_name = "Estatística de Entrega"
        verbose_name_plural = "Estatísticas de Entregas"
        ordering = ['-date']
    
    def __str__(self):
        return f"Estatísticas de {self.date}"
    
    @classmethod
    def generate_daily_stats(cls, date=None):
        """Gera estatísticas para uma data específica"""
        if date is None:
            date = timezone.now().date()
        
        # Busca pedidos da data
        orders = Order.objects.filter(
            created_at__date=date
        )
        
        # Calcula estatísticas
        total_orders = orders.count()
        completed_orders = orders.filter(status='delivered').count()
        cancelled_orders = orders.filter(status='cancelled').count()
        failed_orders = orders.filter(status='failed').count()
        
        # Calcula receita
        total_revenue = orders.filter(status='delivered').aggregate(
            total=models.Sum('final_price')
        )['total'] or 0
        
        # Calcula tempo médio de entrega
        delivered_orders = orders.filter(status='delivered')
        delivery_times = []
        for order in delivered_orders:
            if order.picked_up_at and order.delivered_at:
                time_diff = order.delivered_at - order.picked_up_at
                delivery_times.append(int(time_diff.total_seconds() / 60))
        
        average_delivery_time = sum(delivery_times) // len(delivery_times) if delivery_times else 0
        
        # Calcula avaliação média
        ratings = orders.exclude(rating__isnull=True).values_list('rating', flat=True)
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # Calcula satisfação do cliente
        customer_satisfaction = (completed_orders / total_orders * 100) if total_orders > 0 else 0
        
        # Conta motoboys
        active_motoboys = Motoboy.objects.filter(is_active=True, status='available').count()
        total_motoboys = Motoboy.objects.filter(is_active=True).count()
        
        # Cria ou atualiza estatísticas
        stats, created = cls.objects.get_or_create(
            date=date,
            defaults={
                'total_orders': total_orders,
                'completed_orders': completed_orders,
                'cancelled_orders': cancelled_orders,
                'failed_orders': failed_orders,
                'total_revenue': total_revenue,
                'average_delivery_time': average_delivery_time,
                'average_rating': average_rating,
                'customer_satisfaction': customer_satisfaction,
                'active_motoboys': active_motoboys,
                'total_motoboys': total_motoboys,
            }
        )
        
        if not created:
            # Atualiza estatísticas existentes
            stats.total_orders = total_orders
            stats.completed_orders = completed_orders
            stats.cancelled_orders = cancelled_orders
            stats.failed_orders = failed_orders
            stats.total_revenue = total_revenue
            stats.average_delivery_time = average_delivery_time
            stats.average_rating = average_rating
            stats.customer_satisfaction = customer_satisfaction
            stats.active_motoboys = active_motoboys
            stats.total_motoboys = total_motoboys
            stats.save()
        
        return stats

class MotoboyPerformance(models.Model):
    """Modelo para performance individual dos motoboys"""
    
    motoboy = models.ForeignKey(Motoboy, on_delete=models.CASCADE, verbose_name="Motoboy")
    month = models.PositiveIntegerField(verbose_name="Mês")
    year = models.PositiveIntegerField(verbose_name="Ano")
    
    # Métricas de performance
    total_deliveries = models.PositiveIntegerField(default=0, verbose_name="Total de entregas")
    successful_deliveries = models.PositiveIntegerField(default=0, verbose_name="Entregas com sucesso")
    failed_deliveries = models.PositiveIntegerField(default=0, verbose_name="Entregas que falharam")
    
    # Tempo e distância
    total_distance = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Distância total (km)")
    average_delivery_time = models.PositiveIntegerField(default=0, verbose_name="Tempo médio de entrega (minutos)")
    
    # Avaliações
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Avaliação média")
    total_earnings = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Ganhos totais")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    class Meta:
        verbose_name = "Performance do Motoboy"
        verbose_name_plural = "Performance dos Motoboys"
        unique_together = ['motoboy', 'month', 'year']
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"Performance de {self.motoboy.full_name} - {self.month}/{self.year}"
    
    @classmethod
    def generate_monthly_stats(cls, motoboy, month, year):
        """Gera estatísticas mensais para um motoboy"""
        # Busca pedidos do mês
        orders = Order.objects.filter(
            motoboy=motoboy,
            created_at__month=month,
            created_at__year=year
        )
        
        # Calcula estatísticas
        total_deliveries = orders.count()
        successful_deliveries = orders.filter(status='delivered').count()
        failed_deliveries = orders.filter(status='failed').count()
        
        # Calcula distância total
        total_distance = orders.aggregate(
            total=models.Sum('distance_km')
        )['total'] or 0
        
        # Calcula tempo médio de entrega
        delivered_orders = orders.filter(status='delivered')
        delivery_times = []
        for order in delivered_orders:
            if order.picked_up_at and order.delivered_at:
                time_diff = order.delivered_at - order.picked_up_at
                delivery_times.append(int(time_diff.total_seconds() / 60))
        
        average_delivery_time = sum(delivery_times) // len(delivery_times) if delivery_times else 0
        
        # Calcula avaliação média
        ratings = orders.exclude(rating__isnull=True).values_list('rating', flat=True)
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # Calcula ganhos (assumindo que o motoboy recebe 70% do valor da entrega)
        total_earnings = orders.filter(status='delivered').aggregate(
            total=models.Sum('final_price')
        )['total'] or 0
        total_earnings = total_earnings * 0.7  # 70% para o motoboy
        
        # Cria ou atualiza performance
        performance, created = cls.objects.get_or_create(
            motoboy=motoboy,
            month=month,
            year=year,
            defaults={
                'total_deliveries': total_deliveries,
                'successful_deliveries': successful_deliveries,
                'failed_deliveries': failed_deliveries,
                'total_distance': total_distance,
                'average_delivery_time': average_delivery_time,
                'average_rating': average_rating,
                'total_earnings': total_earnings,
            }
        )
        
        if not created:
            # Atualiza performance existente
            performance.total_deliveries = total_deliveries
            performance.successful_deliveries = successful_deliveries
            performance.failed_deliveries = failed_deliveries
            performance.total_distance = total_distance
            performance.average_delivery_time = average_delivery_time
            performance.average_rating = average_rating
            performance.total_earnings = total_earnings
            performance.save()
        
        return performance

class Category(models.Model):
    """Modelo para categorias de produtos"""
    
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(blank=True, verbose_name="Descrição")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Imagem")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Modelo para produtos do cardápio"""
    
    name = models.CharField(max_length=200, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imagem")
    is_available = models.BooleanField(default=True, verbose_name="Disponível")
    is_featured = models.BooleanField(default=False, verbose_name="Destaque")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    
    # Informações nutricionais (opcional)
    calories = models.PositiveIntegerField(blank=True, null=True, verbose_name="Calorias")
    preparation_time = models.PositiveIntegerField(blank=True, null=True, verbose_name="Tempo de preparo (minutos)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['category__order', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.category.name}"
    
    @property
    def formatted_price(self):
        """Retorna o preço formatado"""
        return f"R$ {self.price:.2f}".replace('.', ',')
