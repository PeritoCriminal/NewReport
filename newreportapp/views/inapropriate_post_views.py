from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from newreportapp.models import PostModel

@login_required
def mark_post_inappropriate(request, post_id):
    post = get_object_or_404(PostModel, id=post_id)
    # Verifica se o usuário tem permissão
    if request.user.access_level in ['moderador', 'administrador']:
        post.set_as_inappropriate = True
        post.save()
    return redirect('home')  # Redirecione para a página desejada