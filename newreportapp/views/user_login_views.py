from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings
import os

def user_login_view(request):
    template_name = 'login.html'

    # Inicializa o formulário
    form = AuthenticationForm(request, data=request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Autentica o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Verifica se a imagem do usuário existe e está acessível
            if user.photo and not os.path.exists(user.photo.path):
                user.photo = None  # Remove a foto quebrada
                user.save()  # Atualiza o banco de dados

            # Define o caminho da imagem do usuário ou a imagem padrão
            user_photo = user.photo.url if user.photo else os.path.join(settings.STATIC_URL, 'images/user_default_photo.png')

            # Realiza o login
            login(request, user)

            # Redireciona para a home após o login bem-sucedido
            return redirect('home')  # Substitua 'home' pelo nome correto da URL para a página inicial

        else:
            # Caso o usuário ou senha estejam incorretos, adiciona um erro
            form.add_error(None, 'Nome de usuário ou senha incorretos.')

    # Retorna o template com o formulário (caso a requisição seja GET ou erro no POST)
    return render(request, template_name, {'form': form})
