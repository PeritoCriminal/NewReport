# newreportapp/views/user_register_views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from newreportapp.forms.user_registration_form import UserRegistrationForm
from newreportapp.utils import administrator_required

@administrator_required
def register_user(request):
    if request.method == 'POST':
        print('Médoto POST')
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('formulário validado')
            user = form.save()
            print(user)
            login(request, user)  
            return redirect('index')  
        else:
            print('formulário não validado.')  #Essa msg aparece
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
