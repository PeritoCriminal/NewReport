# newreportapp/forms/report/section_report_form.py

from django import forms
from newreportapp.models import SectionReportModel

class SectionReportForm(forms.ModelForm):
    class Meta:
        model = SectionReportModel
        fields = ['title', 'description']  # Limita os campos a title e description

        # Customizações de widgets
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Descrição e Exame de Local'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite aqui o texto de sua descriçao. Esse campo aceita parágrafos.'}),
        }

        # Texto de ajuda (opcional)
        help_texts = {
            'title': 'Digite o título da seção.',
            'description': 'Forneça uma descrição detalhada para esta seção do relatório.',
        }
