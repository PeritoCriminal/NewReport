# newreportapp/views/report/section_report_views.py - mantenha essa linha ao copiar o arquivo.

from django.shortcuts import render, redirect, get_object_or_404
from newreportapp.forms.report.section_report_form import SectionReportForm
from newreportapp.models import SectionReportModel, HeaderReportModel, ImageReportModel
from django.contrib import messages

def section_report_view(request, id=None, header_report_id=None, template_name='report/partial_section_report_form.html'):
    """
    View para criação ou edição de um SectionReport.
    Se um header_report_id for fornecido, vincula o relatório de cabeçalho ao SectionReport.
    """
    
    # Obtém a instância do HeaderReportModel se o ID for fornecido.
    header_report_instance = None
    if header_report_id:
        header_report_instance = get_object_or_404(HeaderReportModel, id=header_report_id)

    # Verifica se é edição ou criação.
    section_report_instance = None
    action = "Criação"
    if id:
        section_report_instance = get_object_or_404(SectionReportModel, id=id)
        action = "Edição"

    # Obtém a instância de ImageReportModel relacionada, se aplicável.
    image_report_instance = None
    if section_report_instance:
        image_report_instance = ImageReportModel.objects.filter(report_section=section_report_instance) if section_report_instance else []
    # Inicializa o formulário com os dados do POST ou da instância existente.
    form = SectionReportForm(request.POST or None, instance=section_report_instance)

    if request.method == "POST" and form.is_valid():
        # Salva o SectionReport associando ao HeaderReport, se aplicável.
        section_report = form.save(commit=False)
        if header_report_instance:
            section_report.header_report_model = header_report_instance
        section_report.save()
        
        messages.success(request, f"{action} do relatório realizada com sucesso!")
        # Redireciona após o salvamento.
        return redirect('home')  # Substitua 'home' pela URL desejada.

    # Contexto para o template.
    context = {
        'form': form,
        'action': action,
        'header_report_instance': header_report_instance,
        'section_report_instance': section_report_instance,
        'image_report_instance': image_report_instance,
    }

    return render(request, template_name, context)
