# newreportapp/views/create_post_views.py
from django.shortcuts import render, redirect, get_object_or_404
from newreportapp.forms.post_form import PostForm
from newreportapp.models import PostModel
from django.contrib.auth.decorators import login_required
from newreportapp.models import LikePost

@login_required
def create_post_view(request, post_id=None):
    post = get_object_or_404(PostModel, id=post_id) if post_id else None

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
