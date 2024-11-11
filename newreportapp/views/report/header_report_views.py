from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from newreportapp.forms import HeaderReportForm
from newreportapp.models import HeaderReportModel

def header_report_view(request, report_id=None):
    user = request.user
    if report_id:
        header_report = get_object_or_404(HeaderReportModel, id=report_id)
        action = "Editar Relatório"
        reportCaption = 'Edição de Relatório'
    else:
        header_report = HeaderReportModel()
        action = "Cadastrar Relatório"
        reportCaption = 'Novo Relatório'

    # Obtém a data de designação formatada para o formulário
    designatedDate = header_report.designation_date
    designatedFormatedDate = header_report.dateToForm(designatedDate)
    # occurrence_date = header_report.dateToForm(designatedDate)

    if request.method == "POST":
        form = HeaderReportForm(request.POST, instance=header_report, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"{action} realizado com sucesso!")
            return redirect("home")
        else:
            messages.error(request, "Erro ao processar o formulário. Verifique os campos.")
    else:
        initial={
            'designation_date': designatedFormatedDate,
            'occurrence_date': designatedFormatedDate,
            'call_date': designatedFormatedDate,
            'service_date': designatedFormatedDate,
            'occurrence_time': '00:00',
            'call_time': '00:00',
            'service_time': '00:00'
            }
        form = HeaderReportForm(initial, instance=header_report, user=user)

    context = {
        "form": form,
        "designatedFormatedDate": designatedFormatedDate,
        # "occurrence_date": occurrence_date, 
        "action": action,
        "user": user,
        "reportCaption": reportCaption,
    }

    return render(request, "report/header_report.html", context)
