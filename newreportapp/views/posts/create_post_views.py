from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importa o sistema de mensagens
from newreportapp.forms.post_form import PostForm
from newreportapp.models import PostModel  # Importando o modelo de postagens
from newreportapp.models import ComentPostModel  # Importando o modelo de comentários
from django.contrib.auth.decorators import login_required

@login_required
def create_post_view(request, post_id=None):
    post = get_object_or_404(PostModel, id=post_id) if post_id else None

    # Verifica se a postagem já possui comentários
    if post and post.comments.exists():
        messages.error(request, 'Mensagens comentadas não podem ser editadas, somente deletadas.')  # Adiciona a mensagem de erro
        return redirect('home')  # Redireciona para a página inicial

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    posts = PostModel.objects.all().order_by('-created_at')
    return render(request, 'create_post.html', {'form': form, 'posts': posts, 'post': post})
