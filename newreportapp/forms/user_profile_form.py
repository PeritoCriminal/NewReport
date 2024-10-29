# newreport.forms.user_profile_forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from newreportapp.models import CustomUserModel

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ['display_name', 'gender']  # Inclui apenas os campos desejados
        help_texts = {
            'display_name': 'Nome conforme deseja que apareça no laudo. Você pode utilizar os prefixos Dr. ou Dra., se preferir.',
            'gender': 'Este campo é importante para a exibição do texto no laudo, especialmente no que diz respeito à concordância de gênero gramatical.',
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Configura o autofocus no primeiro campo
        self.fields['display_name'].widget.attrs['autofocus'] = True

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' 
            if field_name == 'old_password':                
                field.widget.attrs['placeholder'] = 'Senha atual'
                field.widget.attrs['value'] = '.'
                field.widget.attrs['onfocus'] = "this.value=''"
            elif field_name == 'new_password1':
                field.widget.attrs['placeholder'] = 'Nova senha, caso deseje alterar.'
            elif field_name == 'new_password2':
                field.widget.attrs['placeholder'] = 'Confirme a nova senha'
