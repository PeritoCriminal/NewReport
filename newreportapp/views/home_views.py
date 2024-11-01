# newreportapp/views/home_views.py
from django.shortcuts import render
from newreportapp.models import PostModel

def home_views(request):
    # Inicializa a queryset de postagens vazia
    posts = PostModel.objects.none()  # Começa com uma queryset vazia

    # Verifica se o usuário está autenticado
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        # Filtra postagens
        public_posts = PostModel.objects.filter(privacy='public')  # Postagens públicas
        friend_posts = PostModel.objects.filter(privacy='friends', author__in=request.user.friends.all())  # Postagens compartilhadas por amigos
        user_posts = PostModel.objects.filter(author=request.user)  # Postagens do próprio usuário

        # Une todas as postagens relevantes
        posts = public_posts.union(friend_posts, user_posts).order_by('-created_at')  # Ordena as postagens da mais recente para a mais antiga

    return render(request, 'home.html', {'posts': posts, 'is_authenticated': is_authenticated})
