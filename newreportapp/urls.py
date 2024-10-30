# newreportapp/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register_user, user_login_view, home_views, edit_user_profile_view, create_post_view

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
    path('account/login/', user_login_view, name='login'),
    path('', home_views, name='home'),
    path('account/edit_user_profile/', edit_user_profile_view, name='edit_user_profile'),
    path('create_post', create_post_view, name='create_post'),
    
    # Página inicial
    # path('', index, name='index'),
]
