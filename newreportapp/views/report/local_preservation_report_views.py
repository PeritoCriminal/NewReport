from django.shortcuts import render, get_object_or_404, redirect
from newreportapp.models import SectionReportModel, HeaderReportModel
from newreportapp.forms import SectionReportForm
from django.contrib import messages

def local_preservation_report_view(request, id=None, header_report_id=None):
    subject = "local"
    title = "Preservação do Local"  # Isso é importante
    rota = "edit_preservation_report"

    # Verifica se existe um registro com o mesmo `header_report_id` e `rota`
    existing_report = None
    if header_report_id:
        existing_report = SectionReportModel.objects.filter(
            header_report_id=header_report_id,
            rota=rota
        ).first()

    # Decide entre abrir para edição ou criar novo registro
    if existing_report:
        report = existing_report
        title = report.title
        action = "Edição"
    else:
        report = SectionReportModel()
        action = "Criação"

    # Obtem o `HeaderReportModel` correspondente, se aplicável
    header_report = get_object_or_404(HeaderReportModel, id=header_report_id) if header_report_id else None

    # Cria o formulário
    form = SectionReportForm(
        request.POST or None,
        instance=report,
        initial={
            'title': title,
            'rota': rota,
        }
    )

    if request.method == "POST":
        # Preenche os campos fixos
        if header_report:
            report.header_report = header_report
            report.subject = subject
            report.title = title
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
        'report': report,
        'form': form,
        'action': action,
        'header_report_id': header_report_id,
        'subject': subject,
        'title': title,
        'rota': rota,
    })
