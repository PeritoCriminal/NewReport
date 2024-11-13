# newreportapp/views/report/list_report_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from newreportapp.models import HeaderReportModel

@login_required
def list_reports(request):
    # Verifica se o usuário tem permissão
    if not getattr(request.user, 'is_editor', False):
        return redirect('home')
    # Filtra os relatórios apenas do usuário logado
    reports = HeaderReportModel.objects.filter(reporting_expert=request.user)
    return render(request, 'report/list_report.html', {'reports': reports})
