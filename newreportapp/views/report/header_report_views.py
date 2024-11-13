from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from newreportapp.forms import HeaderReportForm
from newreportapp.models import HeaderReportModel, UserAttributesToReportModel
from django.contrib.auth.decorators import login_required

@login_required
def header_report_view(request, report_id=None):
    if not request.user.is_editor:
        raise PermissionDenied("Você não tem permissão para acessar esta página.")
    user = request.user

    # Verifica se existe um UserAttributesToReportModel associado ao usuário
    try:
        user_attributes = UserAttributesToReportModel.objects.get(user=user)
    except UserAttributesToReportModel.DoesNotExist:
        # Redireciona para a página de criação de atributos do usuário
        return redirect('user_attributes_create')

    # Verifica se é edição ou criação de um novo relatório
    if report_id:
        header_report = get_object_or_404(HeaderReportModel, id=report_id)
        action = "Editar Relatório"
        reportCaption = 'Laudo atualizado'
    else:
        header_report = HeaderReportModel()
        header_report.expert_display_name = user.display_name
        header_report.city = user_attributes.city
        header_report.reporting_expert = user_attributes.user
        action = "Novo Laudo"
        reportCaption = 'Novo Laudo'

    # Obtém a data de designação formatada para o formulário
    designatedDate = header_report.designation_date
    designatedFormatedDate = header_report.dateToForm(designatedDate)

    if request.method == "POST":
        form = HeaderReportForm(request.POST, instance=header_report, user=user)
        if form.is_valid():
            # Atualiza os campos do relatório com os atributos do usuário
            header_report.city = user_attributes.city
            header_report.institute_director = user_attributes.director
            header_report.institute_unit = user_attributes.unit
            header_report.forensic_team_base = user_attributes.team

            form.save()
            messages.success(request, f"{action} - Registro salvo com sucesso!")
            return redirect("home")
        else:
            messages.error(request, "Erro ao processar o formulário. Verifique os campos.")
            # for field_name, field_value in form.cleaned_data.items():
            #    print(f"{field_name}: {field_value}")
            # print('====================')
            # for field, errors in form.errors.items():
            #    print(f"{field}: {errors}")
    else:
        initial = {
            'designation_date': designatedFormatedDate,
            'occurrence_date': designatedFormatedDate,
            'call_date': designatedFormatedDate,
            'service_date': designatedFormatedDate,
            'occurrence_time': '00:00',
            'call_time': '00:00',
            'service_time': '00:00',
        }
        form = HeaderReportForm(initial=initial, instance=header_report, user=user)

    context = {
        "form": form,
        "designatedFormatedDate": designatedFormatedDate,
        "action": action,
        "user": user,
        "reportCaption": reportCaption,
    }

    return render(request, "report/header_report.html", context)
