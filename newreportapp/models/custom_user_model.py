from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from stdimage import StdImageField
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class CustomUserModel(AbstractUser):
    # Níveis de acesso
    VIEWER = 'viewer'
    EDITOR = 'editor'
    MODERATOR = 'moderator'
    ADMINISTRATOR = 'administrator'

    ACCESS_LEVEL_CHOICES = [
        (VIEWER, 'Viewer'),
        (EDITOR, 'Editor'),
        (MODERATOR, 'Moderador'),
        (ADMINISTRATOR, 'Administrador'),
    ]

    access_level = models.CharField(
        max_length=20,
        choices=ACCESS_LEVEL_CHOICES,
        default=VIEWER,
    )

    display_name = models.CharField(max_length=100, blank=True, null=True)  # Nome para exibição
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True, null=True)  # Sexo

    photo = StdImageField(
        upload_to='user_photos/',
        blank=True,
        null=True,
    )

    is_verified = models.BooleanField(default=False)

    # Adicionando unique=True para o campo email
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        # Exclui a imagem antiga, se existir
        if self.pk:  # Apenas se o objeto já existir
            old_instance = CustomUserModel.objects.get(pk=self.pk)
            if old_instance.photo and old_instance.photo != self.photo:
                # Remove a imagem antiga do armazenamento
                if default_storage.exists(old_instance.photo.name):
                    default_storage.delete(old_instance.photo.name)

        # Redimensiona a imagem antes de salvá-la
        if self.photo:
            img = Image.open(self.photo)
            max_width = 1200  # largura máxima para notebook

            # Redimensiona a imagem se ela for maior que o tamanho máximo
            if img.width > max_width:
                output = BytesIO()
                # Redimensiona mantendo a proporção
                img = img.resize((max_width, int(img.height * (max_width / img.width))), Image.LANCZOS)
                img.save(output, format='JPEG', quality=85)  # Ajuste de qualidade
                output.seek(0)

                # Substitui a imagem original pela versão redimensionada
                self.photo = InMemoryUploadedFile(
                    output, 'ImageField', f"{self.photo.name.split('.')[0]}.jpg", 'image/jpeg',
                    sys.getsizeof(output), None
                )

        super().save(*args, **kwargs)

    ALLOWED_EMAIL_DOMAINS = ['@policiacientifica.sp.gov.br', '@policiacivil.sp.gov.br']

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
