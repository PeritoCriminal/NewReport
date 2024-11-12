# newreportapp/forms/report/header_report_form.py

from django import forms
from newreportapp.models import HeaderReportModel

class HeaderReportForm(forms.ModelForm):
    class Meta:
        model = HeaderReportModel
        fields = [
            'designation_date', 'protocol_number', 'occurrence_date', 'occurrence_time', 'call_date', 'call_time',
            'service_date', 'service_time', 'report_number', 'police_report_number', 'examination_objective',
            'incident_nature', 'police_station', 'requesting_authority', 
            ]
        widgets = {
            'report_number':forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150,'placeholder': 'Ex: 23423 ou 23423/1998'}),
            'protocol_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150,'placeholder': 'Ex: L1234 ou L1234/1998'}),
            'police_report_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150,'placeholder': 'Ex: AB1234 ou AB1234/1998'}),
            'police_station': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150,'placeholder': 'Ex: Del. Sec. Limeira Plantão'}),
            'requesting_authority': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150,'placeholder': 'Ex: Dra. Maria Aparecida'}),
            'examination_objective': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150,'placeholder': 'Ex: Efetuar Exame Inicial'}),
            'incident_nature': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150,'placeholder': 'Ex: Constatação de Danos.'}),
            'designation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'occurrence_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'call_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'service_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'occurrence_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'call_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'service_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        help_texts = {
            'report_number': 'Informe apenas o número do laudo. O ano da data de designação será acrescentado automaticamente.',
            'protocol_number': 'Número do protocolo de atendimento ou registro de entrada. O ano da data de designação será acrescentado automaticamente.',
            'police_report_number': 'Número do boletim de ocorrência. O ano da data do boletim será acrescentado automaticamente.',
            'examination_objective': 'Objetivo do exame, conforme especificado na requisição.',
            'incident_nature': 'Natureza da ocorrência, conforme especificado na requisição.',
            'requesting_authority': 'Informe o pronome de tratamento adequado (ex.: Dr. ou Dra.), seguido do nome completo do delegado ou requisitante.'
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o usuário logado
        super().__init__(*args, **kwargs)
        if user:
            pass
        if not self.instance.designation_date:
            self.fields['designation_date'].initial = '2024-11-10'  # Data de exemplo, ajustada conforme necessidade
