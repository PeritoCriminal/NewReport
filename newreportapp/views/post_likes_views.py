# newreportapp/views/post_likes_views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from newreportapp.models import PostModel

@login_required
def post_like(request, post_id):
    post = get_object_or_404(PostModel, id=post_id)

    # Incrementa ou decrementa a contagem de likes
    if f'liked_{post_id}' not in request.session:
        post.likes_count += 1
        request.session[f'liked_{post_id}'] = True  # Marca que o usuário curtiu
    else:
        post.likes_count -= 1
        del request.session[f'liked_{post_id}']  # Remove a marcação para descurtir

    post.save()
    
    # Retorna a nova contagem de likes como JSON
    return JsonResponse({'likes_count': post.likes_count})
