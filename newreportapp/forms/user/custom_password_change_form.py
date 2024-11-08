from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Senha Atual",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha atual'}),
    )
    new_password1 = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nova senha'}),
    )
    new_password2 = forms.CharField(
        label="Confirme a Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a nova senha'}),
    )
