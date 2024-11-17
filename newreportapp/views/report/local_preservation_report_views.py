from django.shortcuts import render, get_object_or_404, redirect
from newreportapp.models import SectionReportModel, HeaderReportModel
from newreportapp.forms import SectionReportForm
from django.contrib import messages

def local_preservation_report_view(request, id=None, header_report_id=None):
    subject = "local"
    title = "Preservação do Local"  # Isso é importante
    rota = "edit_preservation_report"
    
    if id:
        report = get_object_or_404(SectionReportModel, id=id)
        action = "Edição"
    else:
        report = SectionReportModel()
        action = "Criação"
    

    header_report = get_object_or_404(HeaderReportModel, id=header_report_id) if header_report_id else None

    # Passa o valor de `title` para o campo correspondente no formulário
    form = SectionReportForm(
        request.POST or None,
        instance=report,
        initial={'title': title,
                 'rota': rota,}

    )
    
    if request.method == "POST":
        if header_report:
            report.header_report = header_report
            report.subject = subject
            report.title = title  # Atualiza o título no objeto antes de salvar
            report.rota = rota
        
        if form.is_valid():
            section_report = form.save(commit=False)
            section_report.header_report = header_report  
            section_report.subject = subject  
            section_report.save()
            
            messages.success(request, f"{action} do relatório realizada com sucesso!")
            return redirect('show_report', pk=header_report.id) 
        else:
            print(f'Formulário inválido - Erros: {form.errors}')

    return render(request, 'report/local_preservation_report.html', {
        'form': form,
        'action': action,
        'header_report_id': header_report_id,
        'subject': subject,
        'title': title,
        'rota': rota,
    })
