from django.urls import path
from django.contrib.auth import views as auth_views
from .views import change_password_view, edit_user_profile_view, like_comment, like_post, register_user, post_delete_views, user_login_view, home_views, create_post_view, comment_post_view, delete_comment_view, verify_email

urlpatterns = [
    # URLs de redefinição de senha com templates personalizados
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), 
        name='password_reset'
    ),
    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
        name='password_reset_complete'
    ),
    #path('password_change/', change_password_view, name='password_change'),  # Usando a view personalizada
    path('account/password_change/', change_password_view, name='password_change'),
    # URLs relacionadas à conta do usuário
    path('account/register/', register_user, name='register'),
    path('account/login/', user_login_view, name='login'),
    path('', home_views, name='home'),
    
    # path('post/<int:post_id>/like/', post_and_comments_likes_views.post_like, name='post_like'),
    path('post/<int:post_id>/delete/', post_delete_views, name='post_delete'),  # Rota para deletar
    path('comment/<int:comment_id>/delete/', delete_comment_view, name='delete_comment'),

    # path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('comment/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    # path('msg_to_newcomer')

    path('account/edit_user_profile/', edit_user_profile_view, name='edit_user_profile'),
    path('create_post', create_post_view, name='create_post'),
    path('create_post/<int:post_id>/', create_post_view, name='create_post'),
     path('post/<int:post_id>/comment/', comment_post_view, name='comment_post_view'),


]
