from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Modelo de usuário customizado para clientes"""
    
    # Campos básicos
    email = models.EmailField(unique=True, verbose_name="E-mail")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Telefone")
    
    # Endereço
    address = models.TextField(verbose_name="Endereço completo")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado")
    zip_code = models.CharField(max_length=10, verbose_name="CEP")
    
    # Coordenadas para localização
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude")
    
    # Campos de controle
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    # Configurações
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'address', 'city', 'state', 'zip_code']
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def get_full_address(self):
        """Retorna o endereço completo formatado"""
        return f"{self.address}, {self.city} - {self.state}, {self.zip_code}"
    
    def get_coordinates(self):
        """Retorna as coordenadas como tupla"""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None
