# newreportapp/forms/user_registration_form.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from newreportapp.models import CustomUserModel

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'display_name', 'gender', 'password1', 'password2']  # `access_level` removido

        # Widgets personalizados para cada campo do formulário
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome de Usuário'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email',
                'pattern': '|'.join([f".*{domain}" for domain in CustomUserModel.ALLOWED_EMAIL_DOMAINS]),  # Apenas domínios permitidos
                'title': "Somente emails permitidos, como @policiacientifica.sp.gov.br"
            }),
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
            'email':'São aceitos apenas @policiacientifica.sp.gov.br ou @policiacivil.sp.gov.br',
            'password1': 'Sua senha deve conter pelo menos 8 caracteres.',
            'password2': 'Repita a senha para confirmação.',
            'display_name': 'Nome conforme deseja que apareça no laudo. Você pode utilizar os prefixos Dr. ou Dra., se preferir.',
            'gender': 'Este campo é importante para a exibição do texto no laudo, especialmente no que diz respeito à concordância de gênero gramatical.',
        }

    def clean_email(self):
        # Validação para garantir e-mails com domínios permitidos
        email = self.cleaned_data.get('email')
        if not any(email.endswith(domain) for domain in CustomUserModel.ALLOWED_EMAIL_DOMAINS):
            raise forms.ValidationError("O e-mail deve ser de um domínio permitido.")
        
        # Validação para e-mails únicos
        if CustomUserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está registrado.")
        
        return email
