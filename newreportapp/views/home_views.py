# newreport/views/home_views.py
from django.shortcuts import render
from newreportapp.models import PostModel

def home_views(request):
    # Recupera todas as postagens do banco de dados
    posts = PostModel.objects.all().order_by('-created_at')  # Ordena as postagens da mais recente para a mais antiga

    # Verifica se o usuário está autenticado
    is_authenticated = request.user.is_authenticated
    
    return render(request, 'home.html', {'posts': posts, 'is_authenticated': is_authenticated})
