from django.shortcuts import render, get_object_or_404, redirect
from newreportapp.models import HeaderReportModel

def conclusion_view(request, header_report_id=None):
    # Obtém o `HeaderReportModel` correspondente, se aplicável.
    header_report = get_object_or_404(HeaderReportModel, id=header_report_id)

    # Placeholder para o campo `description` (opcional, pode ser usado diretamente no template).
    place_holder_for_description = """Campo opcional.
    Utilize esse campo para descrever a conclusão de seu relatório."""

    if request.method == "POST":
        # Atualiza a conclusão com o valor enviado pelo formulário.
        header_report.conclusion = request.POST.get('conclusion_description', '').strip()
        header_report.save()
        return redirect('show_report', pk=header_report.id)  # Redireciona para uma página específica após salvar.

    return render(request, 'report/conclusion_report.html', {
        'place_holder_for_description': place_holder_for_description,
        'header_report': header_report,
    })