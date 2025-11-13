from django.core.management.base import BaseCommand
from authentication.models import Permission, RolePermission

class Command(BaseCommand):
    help = 'Set up default role-based permissions'

    def handle(self, *args, **options):
        # Define role-based permissions
        role_permissions = {
            'admin': [
                # Admin has all permissions
                'view_products', 'add_products', 'edit_products', 'delete_products',
                'view_categories', 'add_categories', 'edit_categories', 'delete_categories',
                'view_sales', 'add_sales', 'edit_sales', 'delete_sales', 'process_pos_sales',
                'view_purchases', 'add_purchases', 'edit_purchases', 'delete_purchases',
                'view_customers', 'add_customers', 'edit_customers', 'delete_customers',
                'view_suppliers', 'add_suppliers', 'edit_suppliers', 'delete_suppliers',
                'view_expenses', 'add_expenses', 'edit_expenses', 'delete_expenses',
                'view_reports', 'export_reports',
                'view_users', 'add_users', 'edit_users', 'delete_users', 'assign_permissions',
                'view_settings', 'edit_settings'
            ],
            'manager': [
                # Manager has most permissions except user management
                'view_products', 'add_products', 'edit_products', 'delete_products',
                'view_categories', 'add_categories', 'edit_categories', 'delete_categories',
                'view_sales', 'add_sales', 'edit_sales', 'delete_sales', 'process_pos_sales',
                'view_purchases', 'add_purchases', 'edit_purchases', 'delete_purchases',
                'view_customers', 'add_customers', 'edit_customers', 'delete_customers',
                'view_suppliers', 'add_suppliers', 'edit_suppliers', 'delete_suppliers',
                'view_expenses', 'add_expenses', 'edit_expenses', 'delete_expenses',
                'view_reports', 'export_reports',
                'view_settings'
            ],
            'stock_manager': [
                # Stock manager focuses on products and inventory
                'view_products', 'add_products', 'edit_products',
                'view_categories', 'add_categories', 'edit_categories',
                'view_purchases', 'add_purchases', 'edit_purchases',
                'view_suppliers', 'add_suppliers', 'edit_suppliers'
            ],
            'cashier': [
                # Cashier can process sales and view basic info
                'view_products',
                'process_pos_sales',
                'view_customers', 'add_customers'
            ]
        }
        
        # Set up role permissions
        created_count = 0
        for role, permissions in role_permissions.items():
            for perm_name in permissions:
                try:
                    permission = Permission.objects.get(name=perm_name)
                    role_perm, created = RolePermission.objects.get_or_create(
                        role=role,
                        permission=permission
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(f"Assigned {perm_name} to {role}")
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"Permission {perm_name} not found, skipping...")
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully assigned {created_count} role permissions')
        )