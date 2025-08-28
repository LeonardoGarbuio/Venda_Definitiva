from django.db import models
from django.conf import settings
from motoboys.models import Motoboy
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class MenuItem(models.Model):
    """Modelo para itens do cardápio"""
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço")
    image = models.ImageField(upload_to='menu_items/', verbose_name="Imagem", null=True, blank=True)
    category = models.CharField(max_length=50, verbose_name="Categoria", default="Lanches")
    is_available = models.BooleanField(default=True, verbose_name="Disponível")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item do Cardápio"
        verbose_name_plural = "Itens do Cardápio"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} - R$ {self.price}"

class CartItem(models.Model):
    """Modelo para itens no carrinho"""
    session_key = models.CharField(max_length=40, verbose_name="Chave da Sessão")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="Item")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"
        unique_together = ['session_key', 'menu_item']

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"

    @property
    def total_price(self):
        return self.menu_item.price * self.quantity

class Order(models.Model):
    """Modelo para pedidos de entrega"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('accepted', 'Aceito'),
        ('picked_up', 'Retirado'),
        ('in_transit', 'Em trânsito'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
        ('failed', 'Falhou'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baixa'),
        ('normal', 'Normal'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    # Identificação
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Número do pedido")
    
    # Cliente
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="Cliente")
    
    # Motoboy (pode ser nulo inicialmente)
    motoboy = models.ForeignKey(Motoboy, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Motoboy")
    
    # Informações da entrega
    pickup_address = models.TextField(verbose_name="Endereço de retirada")
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude de retirada")
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude de retirada")
    
    delivery_address = models.TextField(verbose_name="Endereço de entrega")
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude de entrega")
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude de entrega")
    
    # Detalhes do pedido
    description = models.TextField(verbose_name="Descrição do pedido")
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    dimensions = models.CharField(max_length=100, blank=True, default='Padrão', verbose_name="Dimensões")
    is_fragile = models.BooleanField(default=False, verbose_name="Frágil")
    
    # Status e prioridade
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal', verbose_name="Prioridade")
    
    # Valores
    base_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço base")
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Distância (km)")
    final_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Preço final")
    
    # Avaliação
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True, verbose_name="Avaliação (1-5)"
    )
    feedback = models.TextField(blank=True, verbose_name="Feedback do cliente")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    accepted_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de aceitação")
    picked_up_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de retirada")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de entrega")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    # Campos de controle
    estimated_delivery_time = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tempo estimado de entrega (minutos)")
    actual_delivery_time = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tempo real de entrega (minutos)")
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pedido {self.order_number} - {self.customer.get_full_name()}"
    
    def save(self, *args, **kwargs):
        """Gera número do pedido automaticamente"""
        if not self.order_number:
            import random
            import string
            self.order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)
    
    def get_pickup_coordinates(self):
        """Retorna coordenadas de retirada como tupla"""
        if self.pickup_latitude and self.pickup_longitude:
            return (float(self.pickup_latitude), float(self.pickup_longitude))
        return None
    
    def get_delivery_coordinates(self):
        """Retorna coordenadas de entrega como tupla"""
        if self.delivery_latitude and self.delivery_longitude:
            return (float(self.delivery_latitude), float(self.delivery_longitude))
        return None
    
    def can_be_accepted(self):
        """Verifica se o pedido pode ser aceito"""
        return self.status == 'pending' and not self.motoboy
    
    def accept_order(self, motoboy):
        """Aceita o pedido com um motoboy"""
        from django.utils import timezone
        if self.can_be_accepted():
            self.motoboy = motoboy
            self.status = 'accepted'
            self.accepted_at = timezone.now()
            self.save()
            return True
        return False
    
    def pickup_order(self):
        """Marca o pedido como retirado"""
        from django.utils import timezone
        if self.status == 'accepted':
            self.status = 'picked_up'
            self.picked_up_at = timezone.now()
            self.save()
            return True
        return False
    
    def deliver_order(self):
        """Marca o pedido como entregue"""
        from django.utils import timezone
        if self.status == 'picked_up':
            self.status = 'delivered'
            self.delivered_at = timezone.now()
            self.save()
            return True
        return False
    
    def get_status_display_pt(self):
        """Retorna o status em português"""
        status_dict = dict(self.STATUS_CHOICES)
        return status_dict.get(self.status, self.status)
    
    def get_priority_display_pt(self):
        """Retorna a prioridade em português"""
        priority_dict = dict(self.PRIORITY_CHOICES)
        return priority_dict.get(self.priority, self.priority)
    
    def calculate_final_price(self):
        """Calcula o preço final baseado na distância"""
        if self.distance_km:
            # Lógica de cálculo de preço por km
            price_per_km = 2.50  # R$ 2,50 por km
            self.final_price = self.base_price + (float(self.distance_km) * price_per_km)
            self.save(update_fields=['final_price'])
        return self.final_price
