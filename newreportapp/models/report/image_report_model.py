# newreportapp/models/report/image_report_model.py

from django.db import models
from stdimage import StdImageField
from newreportapp.models import SectionReportModel
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class ImageReportModel(models.Model):
    report_section = models.ForeignKey(
        SectionReportModel,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Seção do Relatório"
    )
    description = models.TextField('Descrição', default='', blank=True)
    img = StdImageField(
        upload_to='report_images/',
        verbose_name="Imagem"
    )
    caption = models.CharField(max_length=255, verbose_name="Legenda")
    order = models.PositiveIntegerField(verbose_name="Ordem")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Imagem da Seção do Relatório"
        verbose_name_plural = "Imagens da Seção do Relatório"

    def __str__(self):
        return f"Imagem {self.order} - {self.caption[:20]}"

# Signal para excluir a imagem quando o registro for deletado
@receiver(pre_delete, sender=ImageReportModel)
def delete_image_file(sender, instance, **kwargs):
    """
    Exclui o arquivo de imagem do sistema de arquivos quando o registro ImageReportModel é deletado.
    """
    if instance.img:
        # Verifica se o arquivo realmente existe antes de tentar excluir
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)
