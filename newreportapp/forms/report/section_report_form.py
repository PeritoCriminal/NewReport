# newreportapp/forms/report/section_report_form.py

from django import forms
from newreportapp.models import SectionReportModel

class SectionReportForm(forms.ModelForm):
    class Meta:
        model = SectionReportModel
        fields = ['title', 'description']

        # Customizações de widgets
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-3',  # Adicionando margens e a classe form-control
                'placeholder': 'Ex: Descrição e Exame de Local',
                'default': '# como passar o valor da variável title que está na view? ou faço de outra forma?',
                'aria-label': 'Título da Seção'  # Para melhorar a acessibilidade
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3',  # Adicionando margens e a classe form-control
                'placeholder': 'Digite aqui o texto de sua descrição. Esse campo aceita parágrafos.',
                'aria-label': 'Descrição da Seção',
                'rows': 4  # Ajustando a altura do campo para melhor visualização
            }),
        }

        # Texto de ajuda (opcional)
        help_texts = {
            'title': 'Digite o título da seção. Exemplo: Exame de Local.',
            'description': 'Forneça uma descrição detalhada para esta seção do relatório.',
        }

        # Adicionando classes CSS para os campos e rótulos
        labels = {
            'title': 'Título',
            'description': 'Descrição',
        }
