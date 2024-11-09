from django.db import models
from newreportapp.models import CustomUserModel
from stdimage.models import StdImageField
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class PostModel(models.Model):
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="posts")
    caption = models.CharField('Título', max_length=200, blank=True, default='Imagem e Descrição')
    content = models.TextField()
    image = StdImageField(
        upload_to='posts/images/', null=True, blank=True,
        delete_orphans=True,  # Para deletar imagens antigas que não estão mais em uso
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
    set_as_prohibited = models.BooleanField('Marcado como proibido', default=False)


    def save(self, *args, **kwargs):
        # Se o post já existe (não é novo), verifica se a imagem foi alterada
        if self.pk:  
            original_post = PostModel.objects.get(pk=self.pk)
            # Comparar usando hash ou verificando se a imagem foi alterada
            if original_post.image and self.image and original_post.image != self.image:
                # A imagem foi alterada, processar a imagem
                self._process_image()

        # Se a imagem foi alterada ou não, processa a imagem
        elif self.image:
            self._process_image()

        super().save(*args, **kwargs)

    def _process_image(self):
        # Ajusta a orientação da imagem antes de salvá-la, se necessário
        if self.image:
            img = Image.open(self.image)
            
            # Verifica e aplica a rotação com base na orientação EXIF
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = img._getexif()
                if exif is not None:
                    orientation_value = exif.get(orientation)
                    if orientation_value == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation_value == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation_value == 8:
                        img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # Caso a imagem não tenha metadados EXIF ou a tag não seja encontrada
                pass

            # Redimensiona a imagem se for maior que a largura máxima
            max_width = 1200
            if img.width > max_width:
                img = img.resize((max_width, int(img.height * (max_width / img.width))), Image.LANCZOS)

            # Salva a imagem rotacionada no objeto `image`
            output = BytesIO()
            img.save(output, format='JPEG', quality=85)
            print('\n____________\nImagem salva.\n____________\n')
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output, 'ImageField', f"{self.image.name.split('.')[0]}.jpg", 'image/jpeg',
                sys.getsizeof(output), None
            )

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
