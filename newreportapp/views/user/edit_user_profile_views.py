# newreportapp.views.edit_user_profile_views.py
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from newreportapp.forms import UserProfileForm

@login_required
def edit_user_profile_view(request):
    user = request.user

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user)
        # password_form = CustomPasswordChangeForm(user, request.POST)

        # Verifica se o formulário do perfil é válido
        if profile_form.is_valid():
            profile_form.save()  # Salva as alterações no perfil sem exigir senha
            messages.success(request, 'Perfil atualizado com sucesso!')
            """
            Vamos deixar a troca de senha para outro form e view.
            # Verifica se o formulário de troca de senha foi preenchido corretamente
            if password_form.is_valid():
                user = password_form.save()  # Atualiza a senha
                update_session_auth_hash(request, user)  # Mantém o usuário logado
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('home')
            elif 'new_password1' in request.POST:  # Senha foi enviada, mas está incorreta
                messages.error(request, 'Erro ao alterar a senha. Verifique os dados e tente novamente.')
                #return render(request, 'registration/edit_user_profile.html', {
                #    'profile_form': profile_form,
                #    'password_form': password_form,
                return redirect('home')
                #})
                """
            return redirect('home')           

        else:
            messages.error(request, 'Erro ao atualizar o perfil. Verifique os dados e tente novamente.')

    else:
        profile_form = UserProfileForm(instance=user)
        # password_form = CustomPasswordChangeForm(user)

    return render(request, 'registration/edit_user_profile.html', {
        'profile_form': profile_form,
        # 'password_form': password_form,
    })
