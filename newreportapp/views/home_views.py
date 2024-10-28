#newreport.views.home_views.py
from django.shortcuts import render

def home_views(request):
    return render(request, 'home.html')