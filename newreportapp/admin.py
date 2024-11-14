#newreportapp.admin.py

from django.contrib import admin
from .models import (CustomUserModel,
                     PostModel,
                     ComentPostModel,
                     LikeComment,
                     LikePost,
                     HeaderReportModel,
                     SectionReportModel,
                     UserAttributesToReportModel,
                     )

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

from django.contrib import admin
from .models import LikePost, LikeComment  # Certifique-se de que o caminho está correto

@admin.register(LikePost)
class LikePostModelAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'post', 'post_likes_count')

    def post_likes_count(self, obj):
        # Conta o número total de likes para o post associado
        return LikePost.objects.filter(post=obj.post).count()
    
    post_likes_count.short_description = 'Total Likes on Post'  # Título mais descritivo

@admin.register(LikeComment)
class LikeCommentModelAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'comment', 'comment_likes_count')

    def comment_likes_count(self, obj):
        # Conta o número total de likes para o comentário associado
        return LikeComment.objects.filter(comment=obj.comment).count()
    
    comment_likes_count.short_description = 'Total Likes on Comment'  # Título mais descritivo

@admin.register(HeaderReportModel)
class HeaderReportModelAdmin(admin.ModelAdmin):
    list_display = ('report_number', 'expert_display_name', 'designation_date')

@admin.register(SectionReportModel)
class SectionReportModelAdmin(admin.ModelAdmin):
    list_display = ('header_report', 'subject', 'order', 'title', 'description')

@admin.register(UserAttributesToReportModel)
class UserAttributesToReportModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'city', 'unit', 'team')