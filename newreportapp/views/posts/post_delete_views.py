# newreportapp/views/post_delete_views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from newreportapp.models import PostModel, ComentPostModel

@login_required
def post_delete_views(request, post_id):
    post = get_object_or_404(PostModel, id=post_id)

    # Verifica se o usuário é o autor do post antes de deletar
    if request.user == post.author:
        post.delete()  # Deleta o post
        print('Postagem deletada - post_id')
        return JsonResponse({'success': True})
    
    print('Postagem dnão eletada - post_id')
    return JsonResponse({'success': False})
