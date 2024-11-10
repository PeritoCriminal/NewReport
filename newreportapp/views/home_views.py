from django.shortcuts import render
from django.core.paginator import Paginator
from newreportapp.models import PostModel
from django.contrib import messages

def home_views(request):
    # Inicializa a queryset de postagens vazia
    posts = PostModel.objects.none()

    # Verifica se o usuário está autenticado
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        # Filtra postagens públicas que não são inapropriadas, não são proibidas e do autor ativo
        public_posts = PostModel.objects.filter(
            privacy='public',
            set_as_inappropriate=False,
            set_as_prohibited=False,
            author__is_active=True  # Filtra apenas postagens de autores ativos
        )

        # Filtra postagens do usuário, considerando também se o usuário está ativo
        user_posts = PostModel.objects.filter(
            author=request.user,
            author__is_active=True  # Verifica se o usuário autor da postagem está ativo
        )

        # Une todas as postagens relevantes
        posts = public_posts.union(user_posts).order_by('-updated_at')

    # Configura a paginação com 10 postagens por página
    paginator = Paginator(posts, 10)  # 10 postagens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Adiciona a contagem de likes a cada post
    for post in page_obj:
        post.likes_count = post.likes.count()  # Adiciona um atributo likes_count a cada post
        # if post.set_as_inappropriate:
        #    messages.error(request, "Um dos moderadores ou administrador removeu a publicidade dessa postagem. Ela não será mais exibida publicamente. Você pode fazer uma nova postagem, mas lembre-se de que as postagens devem estar de acordo com as regras.")

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'is_authenticated': is_authenticated,
        # 'user': user,
    })
