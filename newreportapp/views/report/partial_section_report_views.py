# newreportapp/views/report/section_report_views.py

from django.shortcuts import render, redirect, get_object_or_404
from newreportapp.forms import SectionReportForm
from newreportapp.models import SectionReportModel

def section_report_view(request, id=None, template_name='report/partial_section_report_form.html'):
    instance = get_object_or_404(SectionReportModel, id=id) if id else None
    form = SectionReportForm(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('nome_da_pagina_de_sucesso')

    return render(request, template_name, {'form': form})

