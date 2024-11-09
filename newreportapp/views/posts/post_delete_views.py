# newreportapp/views/post_delete_views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from newreportapp.models import PostModel
from django.contrib import messages

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


from django.contrib.auth.decorators import login_required

@login_required
def restore_post(request, post_id):
    # Obtém a postagem ou retorna um erro 404 se não for encontrada
    post = get_object_or_404(PostModel, id=post_id)

    # Verifica se o usuário atual é o autor da postagem ou possui permissão para restaurar
    if request.user == post.author or request.user.has_perm('app_name.restore_post'):
        # Define o campo `set_as_inappropriate` como False para restaurar a visibilidade
        post.set_as_inappropriate = False
        post.save()
        
        # Mensagem de sucesso para feedback ao usuário
        messages.success(request, 'A postagem foi restaurada com sucesso.')
    else:
        # Mensagem de erro caso o usuário não tenha permissão
        messages.error(request, 'Você não tem permissão para restaurar esta postagem.')

    # Redireciona o usuário para uma página específica após a ação
    return redirect('home')  # Substitua pelo nome correto da página de redirecionamento