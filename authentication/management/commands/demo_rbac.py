from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from authentication.decorators import permission_required, role_required

User = get_user_model()

class Command(BaseCommand):
    help = 'Demonstrate RBAC functionality'

    def handle(self, *args, **options):
        # Get a test user
        try:
            user = User.objects.get(username='testuser')
            self.stdout.write(f"Testing permissions for user: {user.username} (role: {user.role})")
            
            # Test role-based access
            self.stdout.write(f"User has 'view_products' permission: {user.has_custom_permission('view_products')}")
            self.stdout.write(f"User has 'add_products' permission: {user.has_custom_permission('add_products')}")
            self.stdout.write(f"User has 'edit_products' permission: {user.has_custom_permission('edit_products')}")
            
            # Explain why these permissions are granted/denied
            if user.has_custom_permission('view_products'):
                self.stdout.write("- 'view_products' is granted through role-based permissions (cashier role)")
            
            if user.has_custom_permission('add_products'):
                self.stdout.write("- 'add_products' is granted through user-specific permissions")
                
            if not user.has_custom_permission('edit_products'):
                self.stdout.write("- 'edit_products' is denied because it's not assigned to cashier role or user")
                
            self.stdout.write(
                self.style.SUCCESS('RBAC demonstration completed successfully')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Test user not found. Run create_test_users first.')
            )