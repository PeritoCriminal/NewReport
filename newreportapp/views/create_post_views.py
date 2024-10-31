# newreportapp/views/create_post_views.py

from django.shortcuts import render, redirect
from newreportapp.forms.post_form import PostForm
from newreportapp.models.post_model import PostModel
from django.contrib.auth.decorators import login_required

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('create_post')  # Redireciona para ver a postagem criada

    else:
        form = PostForm()

    posts = PostModel.objects.all().order_by('-created_at')  # Obtém todas as postagens

    return render(request, 'create_post.html', {'form': form, 'posts': posts})
