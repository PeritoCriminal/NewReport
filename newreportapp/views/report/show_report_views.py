from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from newreportapp.models import HeaderReportModel, SectionReportModel, ImageReportModel
from newreportapp.utils import format_text_with_year, ReportDocx  # Função para geração do .docx
from django.contrib.auth.decorators import login_required
from django.conf import settings
import tempfile, os


@login_required
def show_report(request, pk):
    # Obtém o relatório principal
    report = get_object_or_404(HeaderReportModel, pk=pk)
    
    # Obtém as seções relacionadas ao relatório
    sections = SectionReportModel.objects.filter(header_report=report)
    section_local = sections.filter(subject='local')
    
    # Verifica a existência de títulos  newreport
    is_there_preservation = section_local.filter(title='Preservação do Local').exists()
    is_there_description = section_local.filter(title='Descrição do Local').exists()
    is_there_clue_and_trace = section_local.filter(title='Elementos Observados').exists()
    is_there_collected_items = sections.filter(title='Elementos Coletados').exists()
    is_there_perinecroscopic = sections.filter(title='Exame Perinecroscópico').exists()

    # Formata os números dos relatórios
    num_report = format_text_with_year(report.report_number, report.designation_date)
    num_occurrency = format_text_with_year(report.police_report_number, report.occurrence_date)
    num_protocol = format_text_with_year(report.protocol_number, report.service_date)

    # Organiza imagens agrupadas por seções
    images = ImageReportModel.objects.filter(report_section__in=sections)

    # Pré-processa seções e imagens para enviar ao template
    sections_data = []
    global_image_index = 1  # Contador global para imagens

    for section_index, section in enumerate(sections, start=1):
        section_images = images.filter(report_section=section)
        section_data = {
            'title': section.title,
            'description': section.description,
            'number': section_index,
            'images': [],
        }
        
        for img in section_images:
            section_data['images'].append({
                'subtitle': img.subtitle,
                'description': img.description,
                'img_url': img.img.url,
                'caption': img.caption,
                'subtitle_number': f"{section_index}.{global_image_index}",
                'image_number': global_image_index,
            })
            global_image_index += 1

        sections_data.append(section_data)

    # Verifica se o .docx foi solicitado
    if request.GET.get("generate_docx"):
        header_report_image = os.path.join(settings.BASE_DIR, 'newreportapp', 'static', 'images', 'logos', 'header_report.jpg')

        # Cria um arquivo temporário para o relatório .docx
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
            filepath = temp_file.name

        myDoc = ReportDocx(filepath, header_report_image)

        myDoc.generateTitle0(f'Laudo {num_report}')

        myDoc.generatePreamble(report.makePreamble())

        myDoc.saveDoc()

        
        # Retorna o arquivo como resposta
        response = FileResponse(open(filepath, "rb"), as_attachment=True, filename=f"report_{pk}.docx")
        
        # Exclui o arquivo temporário após o envio
        response.closed_file = lambda: os.remove(filepath) if os.path.exists(filepath) else None

        return response

    # Contexto para o template
    context = {
        'report': report,
        'sections_data': sections_data,
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
    }
    return render(request, 'report/show_report.html', context)
