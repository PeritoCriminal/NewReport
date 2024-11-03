#newreportapp.admin.py

from django.contrib import admin
from .models import CustomUserModel, PostModel, ComentPostModel

@admin.register(CustomUserModel)  # Usando o decorador para registrar o modelo
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'display_name', 'gender', 'access_level')  # Campos a serem exibidos
    search_fields = ('username', 'email', 'display_name')  # Campos pesquisáveis
    list_filter = ('gender', 'access_level')  # Filtros disponíveis

@admin.register(PostModel)  # Usando o decorador correto para registrar o modelo
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('author', 'caption', 'created_at', 'updated_at')  # Campos a serem exibidos
    search_fields = ('author', 'created_at', 'updated_at')  # Campos pesquisáveis
    list_filter = ('privacy',)  # Filtros disponíveis

@admin.register(ComentPostModel)  # Usando o decorador correto para registrar o modelo
class CommentPostModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content')  # Campos a serem exibidos
    search_fields = ('user', 'post')  # Campos pesquisáveis
    list_filter = ('user', 'post', 'content')  # Filtros disponíveis
