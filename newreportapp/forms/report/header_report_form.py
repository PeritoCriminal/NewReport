from django import forms
from newreportapp.models import HeaderReportModel

class HeaderReportForm(forms.ModelForm):
    class Meta:
        model = HeaderReportModel
        fields = [
            'designation_date', 'protocol_number', 'occurrence_date', 'occurrence_time', 'call_date', 'call_time',
            'service_date', 'service_time', 'report_number', 'city', 'police_report_number', 'examination_objective',
            'incident_nature', 'police_station', 'requesting_authority', 'institute_director', 'institute_unit',
            'forensic_team_base', 'expert_display_name', 'reporting_expert', 'considerations', 'conclusion'
        ]
        widgets = {
            'designation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'occurrence_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'call_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'service_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'occurrence_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'call_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'service_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'considerations': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'conclusion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o usuário logado
        super().__init__(*args, **kwargs)
        if user:
            self.fields['expert_display_name'].initial = user.username  # Define o nome do perito como nome de usuário
            self.fields['reporting_expert'].initial = user  # Preenche com o usuário logado (se necessário)
        
        # Garantir que a data da designação esteja no formato correto, se não for preenchida
        if not self.instance.designation_date:
            self.fields['designation_date'].initial = '2024-11-10'  # Data de exemplo, ajustada conforme necessidade
