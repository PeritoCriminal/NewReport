# newreportapp.views.comment_post_views.py

from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from newreportapp.models.post_model import PostModel
from newreportapp.models.comment_post_model import ComentPostModel
from newreportapp.forms import CommentForm

@login_required
def comment_post_view(request, post_id):
    post = get_object_or_404(PostModel, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            # Retorna a resposta com os detalhes do comentário
            return JsonResponse({
                'message': 'Comentário adicionado com sucesso!',
                'username': comment.user.username,
                'content': comment.content,  # Adicione o conteúdo do comentário para exibição
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Formato opcional
            }, status=201)  # 201 Created
        else:
            return JsonResponse({'error': 'Erro ao adicionar o comentário.'}, status=400)  # 400 Bad Request
            
    return JsonResponse({'error': 'Método não permitido.'}, status=405)  # 405 Method Not Allowed
