# newreportapp/models/custom_user_model.py
from django.contrib.auth.models import AbstractUser
from django.db import models

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
