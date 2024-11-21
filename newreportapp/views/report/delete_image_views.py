from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from newreportapp.models import ImageReportModel

def delete_image_view(request, pk):
    """
    View para excluir uma imagem associada a um relatório.
    """
    image_instance = get_object_or_404(ImageReportModel, pk=pk)

    # Confirme a exclusão apenas para requisições POST (melhor prática)
    if request.method == "POST":
        image_instance.delete()
        messages.success(request, "Imagem excluída com sucesso!")
        # Redirecione para a página anterior ou outra página
        return redirect('show_report', pk=image_instance.report_section.header_report.id)

    # Exibir página de confirmação (opcional)
    messages.warning(request, "A exclusão só é permitida via POST.")
    return redirect('show_report', pk=image_instance.report_section.header_report.id)
