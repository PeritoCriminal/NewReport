# newreportapp/views/report/show_report_views.py

from django.shortcuts import render, get_object_or_404
from newreportapp.models import HeaderReportModel

def show_report(request, pk):
    report = get_object_or_404(HeaderReportModel, pk=pk)
    return render(request, 'report/show_report.html', {'report': report})
