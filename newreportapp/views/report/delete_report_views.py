# newreportapp/views/report/delete_report_views.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from newreportapp.models import HeaderReportModel

@login_required
def delete_report(request, report_id):
    # Verifica se o relatório existe e se o usuário logado é o proprietário
    report = get_object_or_404(HeaderReportModel, id=report_id, reporting_expert=request.user)
    
    # Deleta o relatório
    report.delete()

    # Redireciona para a lista de relatórios após a exclusão
    return redirect('list_reports')  # Sub