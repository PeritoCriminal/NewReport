# newreportapp/views/post_and_comments_likes_views.py

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from newreportapp.models import LikePost, ComentPostModel, LikeComment, PostModel

@login_required
def like_post(request, post_id):
    # Primeiro, busca o post pelo post_id para garantir que existe
    post = get_object_or_404(PostModel, id=post_id)

    # Em seguida, procura ou cria o 'LikePost' usando o usuário e o post
    like, created = LikePost.objects.get_or_create(user=request.user, post=post)

    if not created:
        # Se já existe, significa que o usuário quer remover o like
        like.delete()
        message = "Unliked post"
    else:
        # Se foi criado agora, o usuário está curtindo o post
        message = "Liked post"

    # Atualiza a contagem de likes do post
    likes_count = post.likes.count()
    return JsonResponse({"message": message, "likes_count": likes_count})


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(ComentPostModel, id=comment_id)
    like, created = LikeComment.objects.get_or_create(user=request.user, comment=comment)

    if not created:
        # O like já existe, então o usuário está tentando descurtir
        like.delete()
        message = "Unliked comment"
    else:
        # Um novo like foi criado
        message = "Liked comment"

    likes_count = comment.likes.count()  # Atualiza a contagem de likes
    return JsonResponse({"message": message, "likes_count": likes_count})
