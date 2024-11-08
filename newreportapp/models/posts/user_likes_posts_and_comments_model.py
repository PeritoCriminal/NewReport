# newreportapp/models/user_likes_posts_and_comments_model.py

from django.db import models
from newreportapp.models import CustomUserModel, PostModel, ComentPostModel

class LikePost(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="liked_posts")
    post = models.ForeignKey('newreportapp.PostModel', on_delete=models.CASCADE, related_name="likes")  # Use o caminho completo
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked {self.post}"

class LikeComment(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="liked_comments")
    comment = models.ForeignKey('newreportapp.ComentPostModel', on_delete=models.CASCADE, related_name="likes")  # Use o caminho completo
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} liked comment {self.comment.id}"
