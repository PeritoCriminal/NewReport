# newreportapp/urls.py
from django.urls import path
from .views import register_user, UserLoginView, home_views, index, EditUserProfileView  # Certifique-se de que a view foi importada

urlpatterns = [
    path('account/register/', register_user, name='register'),
    path('account/login/', UserLoginView.as_view(), name='login'),
    path('account/home/', home_views, name='home'),
    path('account/edit-profile/', EditUserProfileView, name='edit_profile'),  # URL para editar o perfil
    path('', index, name='index'),
]
