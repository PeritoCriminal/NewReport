#newreportapp.views.create_post_views.py
from django.shortcuts import render

def create_post_view(request):
    return render(request, 'create_post.html')