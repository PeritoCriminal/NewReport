from django.http import JsonResponse
from django.conf import settings
from newreportapp.models import ImageReportModel  # Substitua pelo nome correto do modelo

def load_image_data(request):
    image_id = request.GET.get('image_id')
    
    if not image_id:
        return JsonResponse({'error': 'ID da imagem não fornecido.'}, status=400)
    
    try:
        image = ImageReportModel.objects.get(id=image_id)
        image_data = {
            'id': image.id,
            'url': f"{settings.MEDIA_URL}{image.file}",  # Substitua 'file' pelo campo do modelo que armazena a imagem
            'description': image.description,          # Exemplo: algum dado adicional da imagem
        }
        return JsonResponse(image_data)
    except ImageReportModel.DoesNotExist:
        return JsonResponse({'error': 'Imagem não encontrada.'}, status=404)
