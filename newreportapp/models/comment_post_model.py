#myreportapp.models.comment_post_model.py

from django.db import models
from newreportapp.models import PostModel, CustomUserModel

class ComentPostModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)  # Conteúdo do comentário, limite de 500 caracteres
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação do comentário
    updated_at = models.DateTimeField(auto_now=True)  # Última atualização do comentário (se for editado)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # Para comentários em resposta a outros comentários
    is_active = models.BooleanField(default=True)  # Para permitir desativação de comentários sem deletá-los

    class Meta:
        ordering = ['created_at']  # Ordena os comentários por data de criação

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
