from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from newreportapp.models import CustomUserModel

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ['display_name', 'gender']  # Inclui apenas os campos desejados

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'  # Adiciona classe do Bootstrap

