# newreportapp/forms/user/user_attributes_to_report_form.py

from django import forms
from newreportapp.models import UserAttributesToReportModel

class UserAttributesToReportForm(forms.ModelForm):
    class Meta:
        model = UserAttributesToReportModel
        fields = ['director', 'state', 'city', 'unit', 'team']
        labels = {
            'director': 'Diretor',
            'state': 'Estado',
            'city': 'Cidade',
            'unit': 'Núcleo',
            'team': 'Equipe',
        }
        widgets = {
            'director': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150, 'placeholder':'Ex: Dr. José da Silva ou Dra. Maria Aparecida.'}, ),
            'state': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150, 'placeholder': 'Ex: São Paulo'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150, 'placeholder': 'Ex: Limeira'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150, 'placeholder': 'Ex: Núcleo de Perícias Criminalísticas de Americana'}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150, 'placeholder': 'Ex: EPC - Limeira'}),
        }
        help_texts = {
            'director': 'Preencha este campo com o nome do Diretor do Instituto de Criminalística. O pronome de tratamento (Dr. ou Dra.) será utilizado para identificar o gênero e, assim, editar o preâmbulo do laudo.',
            'unit': 'O nome do Núcleo de Periícias.',
            'team': 'Sua equipe de atendimento.'
        }


    def __init__(self, *args, **kwargs):
        super(UserAttributesToReportForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

