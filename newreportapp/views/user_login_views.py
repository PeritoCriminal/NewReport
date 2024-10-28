# newreport.views.user_login_views
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

def user_login_view(request):
    template_name = 'login.html'
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('home'))
            else:
                form.add_error(None, 'Nome de usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()
    
    return render(request, template_name, {'form': form})
