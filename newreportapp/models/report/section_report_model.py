# newreportapp/models/report/section_report_model.py

from django.db import models
from newreportapp.models import HeaderReportModel

class SectionReportModel(models.Model):
    header_report = models.ForeignKey(
        HeaderReportModel,
        on_delete=models.CASCADE,
        related_name="sections",
        verbose_name="Cabeçalho do Relatório"
    )
    parent_section = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subsections",
        verbose_name="Seção Pai"
    )
    date = models.DateField(auto_now_add=True, verbose_name="Data do Registro")
    
    SUBJECT_CHOICES = [
        ('local', 'Local'),
        ('veiculo', 'Veículo'),
        ('peça', 'Peça'),
        ('cadáver', 'Cadáver'),
        ('impressao_digital', 'Impressão Digital'),
        ('sangue', 'Sangue'),
        ('remessa_ra', 'Remessa para RA'),
        ('remessa_autoridade', 'Remessa para Autoridade'),
        ('outro', 'Outro'),
    ]
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, verbose_name="Assunto")
    
    order = models.PositiveIntegerField(verbose_name="Ordem")
    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    
    class Meta:
        ordering = ['order']
        unique_together = ('header_report', 'order')  # Garante unicidade da ordem por cabeçalho
        verbose_name = "Seção do Relatório"
        verbose_name_plural = "Seções do Relatório"

    def __str__(self):
        return f"{self.title} - {self.get_subject_display()}"
