from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from stdimage import StdImageField
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class CustomUserModel(AbstractUser):
    # Níveis de acesso
    VIEWER = 'viewer'
    # EDITOR = 'editor'
    MODERATOR = 'moderator'
    ADMINISTRATOR = 'administrator'

    ACCESS_LEVEL_CHOICES = [
        (VIEWER, 'Viewer'),
        # (EDITOR, 'Editor'),
        (MODERATOR, 'Moderador'),
        (ADMINISTRATOR, 'Administrador'),
    ]

    access_level = models.CharField(
        max_length=20,
        choices=ACCESS_LEVEL_CHOICES,
        default=VIEWER,
    )

    display_name = models.CharField('Nome para exibição', max_length=100, blank=True, null=True)  # Nome para exibição
    gender = models.CharField('Gênero', max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Não informar')], blank=True, null=True)  # Sexo

    is_editor = models.BooleanField(default=False)

    photo = StdImageField(
        upload_to='user_photos/',
        blank=True,
        null=True,
    )

    is_verified = models.BooleanField(default=False)

    # Adicionando unique=True para o campo email
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)

    ALLOWED_EMAIL_DOMAINS = ['@policiacientifica.sp.gov.br', '@policiacivil.sp.gov.br']

    def save(self, *args, **kwargs):
        # Exclui a imagem antiga, se existir
        if self.pk:  # Apenas se o objeto já existir
            old_instance = CustomUserModel.objects.get(pk=self.pk)
            if old_instance.photo and old_instance.photo != self.photo:
                # Remove a imagem antiga do armazenamento
                if default_storage.exists(old_instance.photo.name):
                    default_storage.delete(old_instance.photo.name)

        # Ajuste de orientação e redimensionamento da imagem antes de salvá-la
        if self.photo:
            img = Image.open(self.photo)
            max_width = 1200  # Largura máxima para visualização em notebook

            # Corrige a orientação da imagem com base nos metadados EXIF
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
            if img.width > max_width:
                img = img.resize((max_width, int(img.height * (max_width / img.width))), Image.LANCZOS)

            # Salva a imagem processada no campo photo
            output = BytesIO()
            img.save(output, format='JPEG', quality=85)
            output.seek(0)
            self.photo = InMemoryUploadedFile(
                output, 'ImageField', f"{self.photo.name.split('.')[0]}.jpg", 'image/jpeg',
                sys.getsizeof(output), None
            )

        super().save(*args, **kwargs)

    def clean(self):
        super().clean()  # Mantém as validações padrão
        if self.email:  # Verifica se o e-mail está preenchido
            # Verifica se o e-mail termina com um dos domínios permitidos
            if not any(self.email.endswith(domain) for domain in self.ALLOWED_EMAIL_DOMAINS):
                raise ValidationError(_("O e-mail deve ser de um domínio permitido: ") + ", ".join(self.ALLOWED_EMAIL_DOMAINS))
            # Verifica se o e-mail já está em uso
            if CustomUserModel.objects.exclude(pk=self.pk).filter(email=self.email).exists():
                raise ValidationError(_("Este e-mail já está em uso."))

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        permissions = [
            ("can_view_content", "Can view content"),
            ("can_edit_content", "Can edit content"),
            ("can_moderate_content", "Can moderate content"),
            ("can_administrate", "Can administrate"),
        ]

    def __str__(self):
        return self.username
