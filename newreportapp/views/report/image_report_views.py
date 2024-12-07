from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from newreportapp.models.report.image_report_model import ImageReportModel, SectionReportModel
from django.core.files.base import ContentFile
from django.contrib import messages
import base64
import os

def save_image_report(request):
    """
    View para salvar ou editar registros de ImageReportModel, salvando imagens em arquivos no diretório de mídia.
    """
    if request.method == "POST":
        # Dados recebidos do formulário
        section_id = request.POST.get('section_id')
        subtitle = request.POST.get('subtitle')
        description = request.POST.get('description', '')
        caption = request.POST.get('caption', '')
        image_data = request.POST.get('image_data', '')  # Base64
        image_id = request.POST.get('image_id')  # Para edição, se existir um ID

        # Valida se o section_id foi enviado
        if not section_id:
            return JsonResponse({
                "success": False,
                "message": "ID da seção é obrigatório."
            }, status=400)

        # Obtém a seção relacionada
        section = get_object_or_404(SectionReportModel, pk=section_id)

        # Decodifica e salva a imagem, se enviada
        decoded_image = None
        if image_data:
            try:
                # Decodificar Base64 e salvar como arquivo
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                file_name = f"image_{section_id}_{image_id or 'new'}.{ext}"
                decoded_image = ContentFile(base64.b64decode(imgstr), name=file_name)
            except Exception as e:
                return JsonResponse({
                    "success": False,
                    "message": f"Erro ao processar a imagem: {str(e)}"
                }, status=400)

        # Verifica se é edição ou criação
        if image_id:
            image_instance = get_object_or_404(ImageReportModel, pk=image_id, report_section=section)
            action = "Edição"
            # Remove a imagem anterior ao atualizar (opcional)
            if decoded_image and image_instance.img:
                if os.path.isfile(image_instance.img.path):
                    os.remove(image_instance.img.path)
        else:
            image_instance = ImageReportModel(report_section=section)
            action = "Criação"
            # Define a ordem para novos registros
            image_instance.order = section.images.count() + 1

        # Atualiza os campos do modelo
        image_instance.description = description
        image_instance.subtitle = subtitle
        image_instance.caption = caption
        if decoded_image:
            image_instance.img = decoded_image

        # Salva o modelo
        image_instance.save()
        messages.success(request, f"{action} - Registro salvo com sucesso!")

        # Retorna uma resposta JSON para atualizar a página
        return JsonResponse({
            "success": True,
            "message": f"{action} da imagem realizada com sucesso!",
            "image_id": image_instance.pk,
            "image_url": image_instance.img.url,
        })

    # Caso não seja POST, retorna erro
    messages.error(request, "Erro ao processar o formulário.")
    return JsonResponse({
        "success": False,
        "message": "Método inválido para esta operação."
    }, status=400)
