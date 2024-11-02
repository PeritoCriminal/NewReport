from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from newreportapp.forms.custom_password_change_form import CustomPasswordChangeForm

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()  # Salva a nova senha
            update_session_auth_hash(request, user)  # Mantém o usuário logado
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('home')  # Redireciona para a página inicial ou outra de sua escolha
        else:
            messages.error(request, 'Erro ao alterar a senha. Verifique os dados e tente novamente.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'registration/password_change_custom.html', {'form': form})
