from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import uuid

class Motoboy(models.Model):
    """Modelo para motoboys do sistema"""
    
    STATUS_CHOICES = [
        ('available', 'Disponível'),
        ('busy', 'Ocupado'),
        ('offline', 'Offline'),
        ('suspended', 'Suspenso'),
    ]
    
    DOCUMENT_TYPE_CHOICES = [
        ('cpf', 'CPF'),
        ('cnh', 'CNH'),
        ('rg', 'RG'),
    ]
    
    # Identificação
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário")
    
    # Dados pessoais
    full_name = models.CharField(max_length=200, verbose_name="Nome completo")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Telefone")
    
    # Documentos
    document_type = models.CharField(max_length=3, choices=DOCUMENT_TYPE_CHOICES, verbose_name="Tipo de documento")
    document_number = models.CharField(max_length=20, unique=True, verbose_name="Número do documento")
    
    # Veículo
    vehicle_model = models.CharField(max_length=100, verbose_name="Modelo da moto")
    vehicle_plate = models.CharField(max_length=10, verbose_name="Placa da moto")
    vehicle_year = models.PositiveIntegerField(verbose_name="Ano da moto")
    vehicle_color = models.CharField(max_length=50, verbose_name="Cor da moto")
    
    # Localização atual
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude atual")
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude atual")
    last_location_update = models.DateTimeField(null=True, blank=True, verbose_name="Última atualização de localização")
    
    # Status e controle
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline', verbose_name="Status")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00, verbose_name="Avaliação")
    total_deliveries = models.PositiveIntegerField(default=0, verbose_name="Total de entregas")
    successful_deliveries = models.PositiveIntegerField(default=0, verbose_name="Entregas com sucesso")
    
    # Dispositivos associados (para identificação única)
    device_ids = models.JSONField(default=list, blank=True, verbose_name="IDs dos dispositivos")
    
    # Campos de controle
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    class Meta:
        verbose_name = "Motoboy"
        verbose_name_plural = "Motoboys"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.vehicle_plate}"
    
    def clean(self):
        """Validação customizada"""
        if self.vehicle_year and self.vehicle_year < 1900:
            raise ValidationError("Ano da moto deve ser maior que 1900")
        
        if self.rating and (self.rating < 0 or self.rating > 5):
            raise ValidationError("Avaliação deve estar entre 0 e 5")
    
    def get_current_location(self):
        """Retorna a localização atual como tupla"""
        if self.current_latitude and self.current_longitude:
            return (float(self.current_latitude), float(self.current_longitude))
        return None
    
    def update_location(self, latitude, longitude):
        """Atualiza a localização atual"""
        from django.utils import timezone
        self.current_latitude = latitude
        self.current_longitude = longitude
        self.last_location_update = timezone.now()
        self.save(update_fields=['current_latitude', 'current_longitude', 'last_location_update'])
    
    def get_success_rate(self):
        """Calcula a taxa de sucesso das entregas"""
        if self.total_deliveries == 0:
            return 0
        return (self.successful_deliveries / self.total_deliveries) * 100
    
    def is_available(self):
        """Verifica se o motoboy está disponível"""
        return self.status == 'available' and self.is_active
    
    def get_status_display_pt(self):
        """Retorna o status em português"""
        status_dict = dict(self.STATUS_CHOICES)
        return status_dict.get(self.status, self.status)
