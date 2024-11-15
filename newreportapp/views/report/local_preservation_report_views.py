from django.shortcuts import render, get_object_or_404, redirect
from newreportapp.models import SectionReportModel, HeaderReportModel
from newreportapp.forms import SectionReportForm
from django.contrib import messages

def local_preservation_report_view(request, id=None, header_report_id=None):
    # Define o tipo de seção específico para essa view
    subject = "local"
    
    # Busca ou cria uma nova instância de SectionReportModel
    if id:
        report = get_object_or_404(SectionReportModel, id=id)
        action = "Edição"
    else:
        report = SectionReportModel()  # Nova instância em caso de criação
        action = "Criação"
    
    # Busca o HeaderReport associado, se o ID estiver presente
    header_report = get_object_or_404(HeaderReportModel, id=header_report_id) if header_report_id else None
    
    # Instancia o formulário com dados do POST ou da instância de report
    form = SectionReportForm(request.POST or None, instance=report)
    
    if request.method == "POST":
        if header_report:
            report.header_report = header_report  # Associa header_report ao report
            report.subject = subject  # Define o campo subject como "local"
        
        if form.is_valid():
            section_report = form.save(commit=False)
            section_report.header_report = header_report  # Confirma a associação com header_report
            section_report.subject = subject  # Define o subject como "local" antes de salvar
            section_report.save()
            
            messages.success(request, f"{action} do relatório realizada com sucesso!")
            return redirect('show_report', pk=header_report.id)  # Aqui preciso passar o id desse relatório, 
        else:
            print(f'Formulário inválido - Erros: {form.errors}')

    # Renderiza o template com o formulário
    return render(request, 'report/local_preservation_report.html', {
        'form': form,
        'action': action,
        'header_report_id': header_report_id,
        'subject': subject,  # Passa o tipo de seção ao template para exibição
    })
