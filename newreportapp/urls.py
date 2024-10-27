# newreportapp/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_user, UserLoginView, home_views, index, EditUserProfileView  # Certifique-se de que a view foi importada

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_user, UserLoginView, home_views, EditUserProfileView, index

urlpatterns = [
    # URLs de redefinição de senha com templates personalizados
    path(
        'password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), 
        name='password_reset'
    ),
    path(
        'password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    path(
        'reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
        name='password_reset_complete'
    ),
    
    # URLs relacionadas à conta do usuário
    path('account/register/', register_user, name='register'),
    path('account/login/', UserLoginView.as_view(), name='login'),
    path('account/home/', home_views, name='home'),
    path('account/edit-profile/', EditUserProfileView, name='edit_profile'),  # URL para editar o perfil

    # Página inicial
    path('', index, name='index'),
]
