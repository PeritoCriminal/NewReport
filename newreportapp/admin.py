from django.contrib import admin
from .models import CustomUserModel

@admin.register(CustomUserModel)  # Usando o decorador para registrar o modelo
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'display_name', 'gender', 'access_level')  # Campos a serem exibidos
    search_fields = ('username', 'email', 'display_name')  # Campos pesquisáveis
    list_filter = ('gender', 'access_level')  # Filtros disponíveis