# newreportapp/views/user/user_attributes_to_report_view.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from newreportapp.models import UserAttributesToReportModel
from newreportapp.forms.user.user_attributes_to_report_form import UserAttributesToReportForm
from django.contrib.auth.decorators import login_required

@login_required
def user_attributes_to_report_view(request, pk=None):
    # Verifica se já existe um registro para o usuário logado
    try:
        instance = UserAttributesToReportModel.objects.get(user=request.user)
        print(f'Editando perfil existente para o usuário: {request.user}')
    except UserAttributesToReportModel.DoesNotExist:
        instance = None
        print('Nenhum perfil existente, criando novo para o usuário logado.')

    if request.method == 'POST':
        form = UserAttributesToReportForm(request.POST, instance=instance)
        
        if form.is_valid():
            new_instance = form.save(commit=False)
            new_instance.user = request.user  # Atribui o usuário logado ao campo `user`
            new_instance.save()  # Salva o registro com o usuário associado
            
            # Mensagem de sucesso
            messages.success(request, 'Perfil salvo com sucesso!')
            return redirect('home')  # Redireciona para uma URL apropriada
        else:
            # Mensagem de erro caso o formulário não seja válido
            messages.error(request, 'Não foi possível salvar o perfil.')
    else:
        form = UserAttributesToReportForm(instance=instance)

    return render(request, 'registration/user_attributes_to_report.html', {'form': form})
