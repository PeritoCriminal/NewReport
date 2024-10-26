# newreportapp/urls.py
from django.urls import path
from .views import register_user, index, UserLoginView, home_views

urlpatterns = [
    path('account/register/', register_user, name='register'),
    path('account/login/', UserLoginView.as_view(), name='login'),
    path('account/home/', home_views, name='home'),
    path('', index, name='index'),
]