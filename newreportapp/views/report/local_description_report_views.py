from django.shortcuts import render, get_object_or_404, redirect
from newreportapp.models import SectionReportModel, HeaderReportModel, ImageReportModel
from newreportapp.forms import SectionReportForm
from django.http import JsonResponse
from django.contrib import messages

def local_description_report_view(request, id=None, header_report_id=None):
    subject = "local"

    # alterar o vlaor do atributo abaixo para diferentes subsecções.
    title = "Descrição do Local"

    # alterar rota com o nome no arquivo URLS
    rota = "edit_description_report"

    existing_report = None
    if header_report_id:
        existing_report = SectionReportModel.objects.filter(
            header_report_id=header_report_id,
            rota=rota
        ).first()

    # Decide entre abrir para edição ou criar novo registro
    if existing_report:
        report_section = existing_report
        title = report_section.title
        action = "Edição"
    else:
        report_section = SectionReportModel()
        action = "Criação"

    # Obtem o `HeaderReportModel` correspondente, se aplicável
    header_report = get_object_or_404(HeaderReportModel, id=header_report_id) if header_report_id else None

    # Obtém as imagens associadas ao report_section
    images = report_section.images.all() if existing_report else []

    # Cria o formulário
    form = SectionReportForm(
        request.POST or None,
        instance=report_section,
        initial={
            'title': title,
            'rota': rota,
        }
    )

    if request.method == "POST":
        # Preenche os campos fixos
        if header_report:
            report_section.header_report = header_report
            report_section.subject = subject
            report_section.title = title
            report_section.rota = rota
        
        if form.is_valid():
            section_report = form.save(commit=False)
            section_report.header_report = header_report
            section_report.subject = subject
            section_report.save()

            messages.success(request, f"{action} do relatório realizada com sucesso!")
            return redirect('show_report', pk=header_report.id)
        else:
            print(f'Formulário inválido - Erros: {form.errors}')

    return render(request, 'report/local_description_report.html', {
        'report_section': report_section,
        'report_section_id': report_section.id,
        'form': form,
        'action': action,
        'header_report_id': header_report_id,
        'subject': subject,
        'title': title,
        'rota': rota,
        'images': images,
    })


def load_image_data(request):
    """Carrega os dados de uma imagem para edição."""
    if request.method == "GET" and 'image_id' in request.GET:
        image_id = request.GET.get('image_id')
        image = get_object_or_404(ImageReportModel, id=image_id)

        data = {
            'id': image.id,
            'description': image.description,
            'caption': image.caption,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Requisição inválida.'}, status=400)
