from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from newreportapp.models import PostModel

@login_required
def mark_post_prohibited(request, post_id):
    post = get_object_or_404(PostModel, id=post_id)
    # Verifica se o usuário tem permissão
    if request.user.access_level in ['administrator']:
        post.set_as_prohibited = True
        post.save()
        print(f'Postagem {post.id} setado como proibido')
    else:
        print(f'{post.id} mantido como apropriado.')
    return redirect('home')  # Redirecione para a página desejada