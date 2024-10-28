#newreport.views.edit_user_profile_views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from newreportapp.forms import UserProfileForm, CustomPasswordChangeForm

@login_required
def edit_user_profile_view(request):
    user = request.user  # Obtém o usuário logado

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        password_form = CustomPasswordChangeForm(user, request.POST)

        # Verifica se o formulário do perfil é válido
        if profile_form.is_valid():
            profile_form.save()  # Salva as alterações no perfil

            # Verifica se o formulário de senha foi preenchido e é válido
            if password_form.is_valid() and password_form.cleaned_data.get('new_password1'):
                user = password_form.save()  # Atualiza a senha
                update_session_auth_hash(request, user)  # Mantém o usuário logado após a troca de senha

            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('home')  # Redireciona para a página inicial ou outra página desejada
        else:
            messages.error(request, 'Erro ao atualizar o perfil. Verifique os dados e tente novamente.')

    else:
        profile_form = UserProfileForm(instance=user)
        password_form = CustomPasswordChangeForm(user)

    return render(request, 'registration/edit_user_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
