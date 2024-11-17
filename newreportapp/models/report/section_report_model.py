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
    
    order = models.PositiveIntegerField(verbose_name="Ordem")  # Preenchido automaticamente
    rota = models.CharField('url',max_length=50, blank=True, default='' )
    subject = models.CharField(max_length=50, verbose_name="Assunto")
    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    
    class Meta:
        ordering = ['order']
        unique_together = ('header_report', 'order')  # Garante unicidade da ordem por cabeçalho
        verbose_name = "Seção do Relatório"
        verbose_name_plural = "Seções do Relatório"

    def __str__(self):
        return f"{self.title} - Ordem {self.order}"

    def save(self, *args, **kwargs):
        # Atribuir automaticamente o próximo valor de `order` se não estiver definido
        if self.order is None:
            last_order = SectionReportModel.objects.filter(header_report=self.header_report).aggregate(
                models.Max('order')
            )['order__max']
            self.order = (last_order or 0) + 1
        super().save(*args, **kwargs)
