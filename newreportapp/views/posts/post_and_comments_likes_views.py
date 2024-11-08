# newreportapp/views/post_and_comments_likes_views.py

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from newreportapp.models import LikePost, ComentPostModel, LikeComment, PostModel

@login_required
def like_post(request, post_id):
    # Busca o post pelo post_id para garantir que existe
    post = get_object_or_404(PostModel, id=post_id)

    # Tenta obter ou criar um like relacionado ao usuário e ao post
    like, created = LikePost.objects.get_or_create(user=request.user, post=post)

    if created:
        # Caso o like tenha sido criado agora, significa que o usuário curtiu o post
        message = "Liked post"
    else:
        # Caso contrário, o like já existia, então removemos para "descurtir"
        like.delete()
        message = "Unliked post"

    # Atualiza a contagem de likes do post
    likes_count = post.likes.count()

    # Retorna o JSON com a mensagem e a contagem atualizada de likes
    return JsonResponse({
        "message": message,
        "likes_count": likes_count
    })


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
