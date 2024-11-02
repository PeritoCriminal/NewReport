# newreportapp/models/custom_user_model.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from stdimage import StdImageField
from django.core.files.storage import default_storage

class CustomUserModel(AbstractUser):
    # Níveis de acesso
    VIEWER = 'viewer'
    EDITOR = 'editor'
    ADMINISTRATOR = 'administrator'

    ACCESS_LEVEL_CHOICES = [
        (VIEWER, 'Viewer'),
        (EDITOR, 'Editor'),
        (ADMINISTRATOR, 'Administrator'),
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
        variations={
            'large': (300, 300),
            'thumbnail': (100, 100, True),
        },
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        # Exclui a imagem antiga, se existir
        if self.pk:  # Apenas se o objeto já existir
            old_instance = CustomUserModel.objects.get(pk=self.pk)
            if old_instance.photo and old_instance.photo != self.photo:
                # Remove a imagem antiga do armazenamento
                if default_storage.exists(old_instance.photo.name):
                    default_storage.delete(old_instance.photo.name)

        super().save(*args, **kwargs)

    ALLOWED_EMAIL_DOMAINS = ['@policiacientifica.sp.gov.br', '@policiacivil.sp.gov.br']

    def clean(self):
        super().clean()  # Mantém as validações padrão
        if self.email:  # Verifica se o e-mail está preenchido
            # Verifica se o e-mail termina com um dos domínios permitidos
            if not any(self.email.endswith(domain) for domain in self.ALLOWED_EMAIL_DOMAINS):
                raise ValidationError("O e-mail deve ser de um domínio permitido: " + ", ".join(self.ALLOWED_EMAIL_DOMAINS))

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        permissions = [
            ("can_view_content", "Can view content"),
            ("can_edit_content", "Can edit content"),
            ("can_administrate", "Can administrate"),
        ]

    def __str__(self):
        return self.username
