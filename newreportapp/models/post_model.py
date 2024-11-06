# newreportapp/models/post_model.py

from django.db import models
from newreportapp.models import CustomUserModel
from stdimage.models import StdImageField
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class PostModel(models.Model):
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="posts")
    caption = models.CharField('Título', max_length=200, blank=True, default='Imagem e Descrição')
    content = models.TextField()
    image = StdImageField(
        upload_to='posts/images/',
        null=True,
        blank=True,
        delete_orphans=True,  # Para deletar imagens antigas não mais em uso
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    privacy = models.CharField(
        max_length=20,
        choices=[("public", "Público"), ("private", "Privado")],
        default="public"
    )
    shared_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="shares")
    set_as_inappropriate = models.BooleanField('Marcado como inapropriado', default=False)

    def save(self, *args, **kwargs):
        # Redimensiona a imagem para uma largura máxima adequada para notebook (por exemplo, 1200px)
        if self.image:
            img = Image.open(self.image)
            max_width = 1200  # largura máxima para exibição em notebook
            
            if img.width > max_width:
                output = BytesIO()
                img = img.resize((max_width, int(img.height * (max_width / img.width))), Image.LANCZOS)
                img.save(output, format='JPEG', quality=85)  # Ajuste de qualidade
                output.seek(0)
                self.image = InMemoryUploadedFile(
                    output, 'ImageField', f"{self.image.name.split('.')[0]}.jpg", 'image/jpeg',
                    sys.getsizeof(output), None
                )
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
