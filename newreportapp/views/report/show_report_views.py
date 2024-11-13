# newreportapp/views/report/show_report_views.py

from django.shortcuts import render, get_object_or_404
from newreportapp.models import HeaderReportModel
from newreportapp.utils import format_text_with_year

def show_report(request, pk):
    report = get_object_or_404(HeaderReportModel, pk=pk)
    num_report = format_text_with_year(report.report_number, report.designation_date)
    num_occurrency = format_text_with_year(report.police_report_number, report.occurrence_date)

    context = {
        'report': report,
        'institute_unit': report.institute_unit,
        'forensic_team_base': report.forensic_team_base,
        'num_report': num_report,
        'num_occurrency': num_occurrency,
    }
    return render(request, 'report/show_report.html', context)
