from django.shortcuts import render, get_object_or_404, redirect
from newreportapp.models import HeaderReportModel

def considerations_view(request, header_report_id=None):
    # Obtém o `HeaderReportModel` correspondente, se aplicável.
    header_report = get_object_or_404(HeaderReportModel, id=header_report_id)

    # Placeholder para o campo `description` (opcional, pode ser usado diretamente no template).
    place_holder_for_description = """Campo opcional.
    Utilize esse campo para apontar considerações de interesse investigatório."""

    if request.method == "POST":
        # Atualiza a conclusão com o valor enviado pelo formulário.
        header_report.considerations = request.POST.get('observations', '').strip()
        header_report.save()
        return redirect('show_report', pk=header_report.id)  # Redireciona para uma página específica após salvar.

    return render(request, 'report/considerations_report.html', {
        'place_holder_for_description': place_holder_for_description,
        'header_report': header_report,
    })
