from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from .models import Permission

def role_required(allowed_roles):
    """
    Decorator to restrict access based on user roles.
    allowed_roles: list of roles that are allowed to access the view
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard:index')
        return _wrapped_view
    return decorator

def permission_required(permission_name):
    """
    Decorator to restrict access based on specific permissions.
    permission_name: name of the permission required to access the view
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.has_custom_permission(permission_name):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard:index')
        return _wrapped_view
    return decorator

def admin_required(view_func):
    """
    Decorator that checks if the user is an admin.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('authentication:login')
        if request.user.role != 'admin':
            messages.error(request, 'You do not have permission to access this page. Only administrators can perform this action.')
            return redirect('dashboard:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def manager_required(view_func):
    """
    Decorator that checks if the user is a manager or admin.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('authentication:login')
        if request.user.role not in ['admin', 'manager']:
            messages.error(request, 'You do not have permission to access this page. Only managers and administrators can perform this action.')
            return redirect('dashboard:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view