from django.shortcuts import render
from django.core.paginator import Paginator
from newreportapp.models import PostModel

def home_views(request):
    # Inicializa a queryset de postagens vazia
    posts = PostModel.objects.none()

    # Verifica se o usuário está autenticado
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        # Filtra postagens
        public_posts = PostModel.objects.filter(privacy='public')
        user_posts = PostModel.objects.filter(author=request.user)

        # Une todas as postagens relevantes
        posts = public_posts.union(user_posts).order_by('-updated_at')

    # Configura a paginação com 10 postagens por página
    paginator = Paginator(posts, 10)  # 10 postagens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Adiciona a contagem de likes a cada post
    for post in page_obj:
        post.likes_count = post.likes.count()  # Adiciona um atributo likes_count a cada post

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'is_authenticated': is_authenticated,
    })
