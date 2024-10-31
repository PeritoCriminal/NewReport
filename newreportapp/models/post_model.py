#newreportapp.models.post_model.py
from django.db import models
from newreportapp.models import CustomUserModel
from stdimage.models import StdImageField

class PostModel(models.Model):
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="posts")
    caption = models.CharField('Título', max_length=200, blank=True, default='Imagem e Descrição')
    content = models.TextField()
    image = StdImageField(
        upload_to='posts/images/', null=True, blank=True,
        variations={
            'large': (1200, 800, True),  # Ajusta para até 1200px de largura mantendo a proporção
            'thumbnail': (300, 200, True)  # Miniatura opcional para otimização de visualização
        },
        delete_orphans=True,  # Para deletar imagens antigas que não estão mais em uso
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.PositiveIntegerField(default=0)
    privacy = models.CharField(
        max_length=20,
        choices=[("public", "Público"), ("friends", "Amigos"), ("private", "Privado")],
        default="public"
    )
    shared_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="shares")

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
