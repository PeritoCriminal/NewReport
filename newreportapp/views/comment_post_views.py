from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone  # Importar timezone para obter a data e hora atuais
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
            
            # Atualiza o campo updated_at do post
            post.updated_at = timezone.now()  # Define a data e hora atuais
            post.save()  # Salva a alteração no banco de dados
            
            # Retorna a resposta com os detalhes do comentário
            return JsonResponse({
                'message': 'Comentário adicionado com sucesso!',
                'username': comment.user.username,
                'content': comment.content,  # Conteúdo do comentário
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Data do comentário
                'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),  # Data de atualização do post
                'user_is_author': comment.user == request.user  # Verificação se o autor é o usuário logado
            }, status=201)  # 201 Created
        else:
            return JsonResponse({'error': 'Erro ao adicionar o comentário.'}, status=400)  # 400 Bad Request
            
    return JsonResponse({'error': 'Método não permitido.'}, status=405)  # 405 Method Not Allowed


@login_required
def delete_comment_view(request, comment_id):
    comment = get_object_or_404(ComentPostModel, id=comment_id)
    post = comment.post  # Supondo que `ComentPostModel` tenha um campo de relacionamento com o post, como `post = ForeignKey(PostModel, ...)`

    # Verifique se o usuário logado é o autor do comentário ou o autor do post
    if request.user != comment.user and request.user != post.author:
        return JsonResponse({'error': 'Você não tem permissão para deletar este comentário.'}, status=403)
    
    # Deleta o comentário se a verificação de permissão passou
    comment.delete()
    return JsonResponse({'message': 'Comentário deletado com sucesso!'}, status=200)
