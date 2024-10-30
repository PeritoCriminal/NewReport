#newreportapp.models.post_model.py
from django.db import models
from newreportapp.models import CustomUserModel

class PostModel(models.Model):
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
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
