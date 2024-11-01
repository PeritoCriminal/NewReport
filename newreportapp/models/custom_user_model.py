# newreportapp/models/custom_user_model.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from stdimage import StdImageField

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

    # Campo de amigos
    friends = models.ManyToManyField('self', symmetrical=True, blank=True, related_name="user_friends")

    # Campo de solicitações pendentes
    friends_pending = models.ManyToManyField('self', symmetrical=False, blank=True, related_name="pending_requests")

    # Lista de domínios permitidos
    ALLOWED_EMAIL_DOMAINS = ['@policiacientifica.sp.gov.br', '@policiacivil.sp.gov.br']

    def clean(self):
        super().clean()  # Mantém as validações padrão
        if self.email:  # Verifica se o e-mail está preenchido
            # Verifica se o e-mail termina com um dos domínios permitidos
            if not any(self.email.endswith(domain) for domain in self.ALLOWED_EMAIL_DOMAINS):
                raise ValidationError("O e-mail deve ser de um domínio permitido: " + ", ".join(self.ALLOWED_EMAIL_DOMAINS))

    # Método para enviar solicitação de amizade
    def send_friend_request(self, user):
        """Enviar solicitação de amizade para outro usuário"""
        user.friends_pending.add(self)

    # Método para aceitar solicitação de amizade
    def accept_friend_request(self, user):
        """Aceitar solicitação de amizade de outro usuário"""
        if user in self.friends_pending.all():
            # Adiciona ambos como amigos e remove a solicitação pendente
            self.friends.add(user)
            self.friends_pending.remove(user)
            user.friends.add(self)
            user.pending_requests.remove(self)  # Remove também do outro lado

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
