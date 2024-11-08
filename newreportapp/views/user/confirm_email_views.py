#newreportapp/views/confirm_email_views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login
from newreportapp.models import CustomUserModel

def confirm_email(request, token):
    # Obtendo o usuário que corresponde ao token de confirmação
    user = get_object_or_404(CustomUserModel, confirmation_token=token)
    
    # Ativa o usuário
    user.is_active = True
    user.save()

    # Login automático após a confirmação
    login(request, user)

    return redirect('complete_registration_form')  # Redireciona para o formulário completo
