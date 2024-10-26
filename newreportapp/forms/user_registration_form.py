# newreportapp/forms/user_registration_form.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from newreportapp.models import CustomUserModel

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'access_level', 'display_name', 'gender', 'password1', 'password2']
        
        # Widgets personalizados para cada campo do formulário
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome de Usuário'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email'
            }),
            'access_level': forms.Select(attrs={
                'class': 'form-control'
            }),  # Supondo que access_level seja um campo de escolha
            'display_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome para Exibição'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Senha'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Confirme a Senha'
            }),
        }

        # Textos de ajuda para orientação ao usuário
        help_texts = {
            'username': 'Obrigatório. 150 caracteres ou menos. Apenas letras, números e @/./+/-/_ .',
            'password1': 'Sua senha deve conter pelo menos 8 caracteres.',
            'password2': 'Repita a senha para confirmação.',
        }

    def clean_email(self):
        # Validação adicional opcional para garantir e-mails únicos
        email = self.cleaned_data.get('email')
        if CustomUserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está registrado.")
        return email
