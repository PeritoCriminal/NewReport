# newreportapp/views/report/image_report_views.py - Preserve essa linha ao copiar o arquivo.

from django.shortcuts import render, get_object_or_404, redirect
from newreportapp.models.report.image_report_model import ImageReportModel, SectionReportModel
from newreportapp.forms.report.image_report_form import ImageReportForm
from django.contrib import messages

def image_report_view(request, section_pk, pk=None):
    """
    View para criar ou editar registros de ImageReportModel.
    """
    # Obtém a seção do relatório
    section = get_object_or_404(SectionReportModel, pk=section_pk)

    # Verifica se é edição ou criação
    if pk:
        instance = get_object_or_404(ImageReportModel, pk=pk, report_section=section)
        action = "Edição"
    else:
        instance = None
        action = "Criação"

    if request.method == "POST":
        form = ImageReportForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            image = form.save(commit=False)
            image.report_section = section  # Relaciona a imagem à seção
            if not instance:  # Define a ordem apenas para novos registros
                image.order = section.images.count() + 1
            image.save()
            messages.success(request, f"{action} da imagem realizada com sucesso!")
            return redirect('section_report_detail', pk=section.pk)  # Redireciona após salvar
        else:
            messages.error(request, "O formulário contém erros. Verifique os campos e tente novamente.")
    else:
        form = ImageReportForm(instance=instance)

    # Acho que não preciso desse context, porque o template é carregado pela view local_preservation_report
    

    return render(request, 'report/image_report.html')
