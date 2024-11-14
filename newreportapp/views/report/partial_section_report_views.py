# newreportapp/views/report/section_report_views.py

from django.shortcuts import render, redirect, get_object_or_404
from newreportapp.forms import SectionReportForm
from newreportapp.models import SectionReportModel, HeaderReportModel
from django.contrib import messages

def section_report_view(request, id=None, header_report_id=None, template_name='report/partial_section_report_form.html'):
    # Verifica se o header_report_id foi passado e se o ID do relatório de cabeçalho é válido
    if header_report_id:
        header_report_instance = get_object_or_404(HeaderReportModel, id=header_report_id)
    else:
        header_report_instance = None

    # Se for edição, carrega a instância do SectionReportModel
    if id:
        section_report_instance = get_object_or_404(SectionReportModel, id=id)
        action = "Edição"
    else:
        section_report_instance = None
        action = "Criação"
    
    # Instancia o formulário com dados de `POST` ou preenche com a instância do SectionReport
    form = SectionReportForm(request.POST or None, instance=section_report_instance)
    
    # Se o formulário for válido, salva a instância e redireciona
    if request.method == "POST" and form.is_valid():
        # Se o header_report_instance foi passado, associamos ao novo SectionReport
        if header_report_instance:
            section_report = form.save(commit=False)
            section_report.header_report_model = header_report_instance
            section_report.save()
            messages.success(request, f"{action} do relatório realizada com sucesso!")
            return redirect('home')  # ou redirecionar para outra página
    
    context = {
        'form': form,
        'action': action,
        'header_report_instance': header_report_instance,  # Para exibir o header_report_instance no template, se necessário
    }
    
    return render(request, template_name, context)
