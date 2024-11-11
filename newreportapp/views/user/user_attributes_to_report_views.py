# newreportapp/views/user/user_attributes_to_report_view.py

from django.shortcuts import render, get_object_or_404, redirect
from newreportapp.models import UserAttributesToReportModel
from newreportapp.forms import UserAttributesToReportForm

def user_attributes_to_report_view(request, pk=None):
    if pk:
        instance = get_object_or_404(UserAttributesToReportModel, pk=pk)
        print(f'Edtar perfil: {pk}')
    else:
        instance = None
        print('Novo perfil')

    if request.method == 'POST':
        form = UserAttributesToReportForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('url_to_redirect_after_save')  # Redirecione para uma URL apropriada
    else:
        form = UserAttributesToReportForm(instance=instance)

    return render(request, 'registration/user_attributes_to_report.html', {'form': form})
