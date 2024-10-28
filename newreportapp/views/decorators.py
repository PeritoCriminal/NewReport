from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps

def administrator_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redireciona para login se o usuário não estiver autenticado
        if request.user.access_level != 'administrator':
            raise PermissionDenied("Você não tem permissão para acessar esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view