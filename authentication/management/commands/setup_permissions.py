from django.core.management.base import BaseCommand
from authentication.models import Permission, RolePermission

class Command(BaseCommand):
    help = 'Set up default permissions for roles'

    def handle(self, *args, **options):
        # Define permissions
        permissions_data = [
            # Product permissions
            {'name': 'view_products', 'description': 'Can view products', 'category': 'products'},
            {'name': 'add_products', 'description': 'Can add products', 'category': 'products'},
            {'name': 'edit_products', 'description': 'Can edit products', 'category': 'products'},
            {'name': 'delete_products', 'description': 'Can delete products', 'category': 'products'},
            
            # Sales permissions
            {'name': 'view_sales', 'description': 'Can view sales', 'category': 'sales'},
            {'name': 'add_sales', 'description': 'Can add sales', 'category': 'sales'},
            {'name': 'edit_sales', 'description': 'Can edit sales', 'category': 'sales'},
            {'name': 'delete_sales', 'description': 'Can delete sales', 'category': 'sales'},
            {'name': 'process_pos', 'description': 'Can process point of sale transactions', 'category': 'sales'},
            
            # Purchase permissions
            {'name': 'view_purchases', 'description': 'Can view purchases', 'category': 'purchases'},
            {'name': 'add_purchases', 'description': 'Can add purchases', 'category': 'purchases'},
            {'name': 'edit_purchases', 'description': 'Can edit purchases', 'category': 'purchases'},
            {'name': 'delete_purchases', 'description': 'Can delete purchases', 'category': 'purchases'},
            
            # Customer permissions
            {'name': 'view_customers', 'description': 'Can view customers', 'category': 'customers'},
            {'name': 'add_customers', 'description': 'Can add customers', 'category': 'customers'},
            {'name': 'edit_customers', 'description': 'Can edit customers', 'category': 'customers'},
            {'name': 'delete_customers', 'description': 'Can delete customers', 'category': 'customers'},
            
            # Supplier permissions
            {'name': 'view_suppliers', 'description': 'Can view suppliers', 'category': 'suppliers'},
            {'name': 'add_suppliers', 'description': 'Can add suppliers', 'category': 'suppliers'},
            {'name': 'edit_suppliers', 'description': 'Can edit suppliers', 'category': 'suppliers'},
            {'name': 'delete_suppliers', 'description': 'Can delete suppliers', 'category': 'suppliers'},
            
            # Expense permissions
            {'name': 'view_expenses', 'description': 'Can view expenses', 'category': 'expenses'},
            {'name': 'add_expenses', 'description': 'Can add expenses', 'category': 'expenses'},
            {'name': 'edit_expenses', 'description': 'Can edit expenses', 'category': 'expenses'},
            {'name': 'delete_expenses', 'description': 'Can delete expenses', 'category': 'expenses'},
            
            # Report permissions
            {'name': 'view_reports', 'description': 'Can view reports', 'category': 'reports'},
            
            # Branch permissions
            {'name': 'view_branches', 'description': 'Can view branches', 'category': 'branches'},
            {'name': 'add_branches', 'description': 'Can add branches', 'category': 'branches'},
            {'name': 'edit_branches', 'description': 'Can edit branches', 'category': 'branches'},
            {'name': 'delete_branches', 'description': 'Can delete branches', 'category': 'branches'},
            {'name': 'switch_branches', 'description': 'Can switch between branches', 'category': 'branches'},
            
            # Settings permissions
            {'name': 'view_settings', 'description': 'Can view settings', 'category': 'settings'},
            {'name': 'edit_settings', 'description': 'Can edit settings', 'category': 'settings'},
        ]
        
        # Create permissions
        permissions = {}
        for perm_data in permissions_data:
            perm, created = Permission.objects.get_or_create(
                name=perm_data['name'],
                defaults={
                    'description': perm_data['description'],
                    'category': perm_data['category']
                }
            )
            permissions[perm_data['name']] = perm
            if created:
                self.stdout.write(f'Created permission: {perm_data["name"]}')
            else:
                self.stdout.write(f'Permission already exists: {perm_data["name"]}')
        
        # Define role permissions
        role_permissions_data = {
            'admin': list(permissions.keys()),  # Admins get all permissions
            'manager': [name for name in permissions.keys() if not name.startswith('delete_')],  # Managers get all except delete
            'cashier': [
                'view_sales', 'add_sales', 'edit_sales', 'process_pos',
                'view_customers', 'add_customers', 'edit_customers'
            ],
            'stock_manager': [
                'view_products', 'add_products', 'edit_products',
                'view_purchases', 'add_purchases', 'edit_purchases',
                'view_suppliers', 'add_suppliers', 'edit_suppliers'
            ]
        }
        
        # Assign permissions to roles
        for role, perm_names in role_permissions_data.items():
            # Clear existing role permissions
            RolePermission.objects.filter(role=role).delete()
            
            # Assign new permissions
            for perm_name in perm_names:
                if perm_name in permissions:
                    RolePermission.objects.get_or_create(
                        role=role,
                        permission=permissions[perm_name]
                    )
            self.stdout.write(f'Assigned {len(perm_names)} permissions to {role} role')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up default permissions for roles')
        )