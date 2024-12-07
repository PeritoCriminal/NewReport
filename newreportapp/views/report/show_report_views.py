# newreportapp/views/report/show_report_views.py

from django.shortcuts import render, get_object_or_404
from newreportapp.models import HeaderReportModel, SectionReportModel, ImageReportModel
from newreportapp.utils import format_text_with_year
from django.contrib.auth.decorators import login_required

@login_required
def show_report(request, pk):
    report = get_object_or_404(HeaderReportModel, pk=pk)
    section = SectionReportModel.objects.filter(header_report=report)
    section_local = SectionReportModel.objects.filter(header_report=report, subject='local')
    is_there_preservation = section_local.filter(title='Preservação do Local').exists()
    is_there_description = section_local.filter(title='Descrição do Local').exists()
    is_there_clue_and_trace = section_local.filter(title='Elementos Observados').exists()
    is_there_collected_items = section.filter(title='Elementos Coletados').exists()
    is_there_perinecroscopic = section.filter(title='Exame Perinecroscópico').exists()
    num_report = format_text_with_year(report.report_number, report.designation_date)
    num_occurrency = format_text_with_year(report.police_report_number, report.occurrence_date)
    num_protocol = format_text_with_year(report.protocol_number, report.service_date)

    images = ImageReportModel.objects.filter(report_section__in=section)

    context = {
        'report': report,
        'section': section, 
        'section_local': section_local,
        'is_there_preservation': is_there_preservation,
        'is_there_description': is_there_description,
        'is_there_clue_and_trace': is_there_clue_and_trace,
        'is_there_collected_items': is_there_collected_items,
        'is_there_perinecroscopic': is_there_perinecroscopic,
        'institute_unit': report.institute_unit,
        'forensic_team_base': report.forensic_team_base,
        'num_report': num_report,
        'num_occurrency': num_occurrency,
        'num_protocol': num_protocol,
        'images': images,
    }
    return render(request, 'report/show_report.html', context)
