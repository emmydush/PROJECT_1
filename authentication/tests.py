from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Permission, RolePermission, UserPermission

User = get_user_model()

class RBACTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='cashier'
        )
        
        # Create test permissions
        self.view_products = Permission.objects.create(
            name='view_products',
            description='Can view products',
            category='products'
        )
        
        self.add_products = Permission.objects.create(
            name='add_products',
            description='Can add products',
            category='products'
        )
        
        # Assign role permission
        RolePermission.objects.create(
            role='cashier',
            permission=self.view_products
        )
        
        # Assign user-specific permission
        UserPermission.objects.create(
            user=self.user,
            permission=self.add_products,
            granted=True
        )

    def test_role_based_permission(self):
        # Test that user has permission through role
        self.assertTrue(self.user.has_custom_permission('view_products'))
        
        # Test that user doesn't have permission not assigned to role
        self.assertFalse(self.user.has_custom_permission('delete_products'))

    def test_user_specific_permission(self):
        # Test that user has user-specific permission
        self.assertTrue(self.user.has_custom_permission('add_products'))
        
    def test_permission_denied(self):
        # Test that user doesn't have unassigned permission
        self.assertFalse(self.user.has_custom_permission('edit_products'))