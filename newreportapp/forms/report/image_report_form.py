# newreportapp/forms/report/image_report_form.py - Preserve essa linha ao copiar o arquivo.

from django import forms
from newreportapp.models.report.image_report_model import ImageReportModel

class ImageReportForm(forms.ModelForm):
    class Meta:
        model = ImageReportModel
        fields = ['description', 'img', 'caption']  # Apenas os campos necessários
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'description': 'Descrição',
            'img': 'Imagem',
            'caption': 'Legenda',
        }
        help_texts = {
            'description': 'Adicione uma descrição opcional para esta imagem.',
            'img': 'Selecione a imagem a ser enviada.',
            'caption': 'Forneça uma legenda para a imagem.',
        }