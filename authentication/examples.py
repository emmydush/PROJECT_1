"""
Examples of how to use the RBAC system in views
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.decorators import permission_required, role_required, admin_required
from authentication.models import User

# Example 1: Restricting access based on specific permissions
@permission_required('view_products')
def product_list_view(request):
    """
    Only users with 'view_products' permission can access this view.
    This includes:
    - Users with the 'view_products' permission assigned directly to them
    - Users whose role includes the 'view_products' permission
    """
    # View logic here
    return render(request, 'products/list.html')

# Example 2: Restricting access based on roles
@role_required(['admin', 'manager'])
def manage_users_view(request):
    """
    Only admin and manager users can access this view.
    This is role-based rather than permission-based.
    """
    users = User.objects.all()
    return render(request, 'authentication/user_management.html', {'users': users})

# Example 3: Admin-only access
@admin_required
def system_settings_view(request):
    """
    Only admin users can access this view.
    """
    # View logic here
    return render(request, 'settings/system.html')

# Example 4: Chaining decorators for more complex access control
@role_required(['admin', 'manager'])
@permission_required('edit_products')
def edit_product_view(request, product_id):
    """
    Only admin or manager users with 'edit_products' permission can access this view.
    """
    # View logic here
    return render(request, 'products/edit.html')

# Example 5: Programmatic permission checking
@login_required
def dashboard_view(request):
    """
    Example of checking permissions programmatically within a view.
    """
    context = {
        'can_view_products': request.user.has_custom_permission('view_products'),
        'can_add_products': request.user.has_custom_permission('add_products'),
        'can_manage_users': request.user.has_custom_permission('manage_users'),
    }
    return render(request, 'dashboard.html', context)