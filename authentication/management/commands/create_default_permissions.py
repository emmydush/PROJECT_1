from django.core.management.base import BaseCommand
from authentication.models import Permission

class Command(BaseCommand):
    help = 'Create default permissions for the system'

    def handle(self, *args, **options):
        # Define default permissions
        default_permissions = [
            # Product permissions
            {'name': 'view_products', 'description': 'Can view products', 'category': 'Products'},
            {'name': 'add_products', 'description': 'Can add new products', 'category': 'Products'},
            {'name': 'edit_products', 'description': 'Can edit existing products', 'category': 'Products'},
            {'name': 'delete_products', 'description': 'Can delete products', 'category': 'Products'},
            
            # Category permissions
            {'name': 'view_categories', 'description': 'Can view product categories', 'category': 'Products'},
            {'name': 'add_categories', 'description': 'Can add new product categories', 'category': 'Products'},
            {'name': 'edit_categories', 'description': 'Can edit existing product categories', 'category': 'Products'},
            {'name': 'delete_categories', 'description': 'Can delete product categories', 'category': 'Products'},
            
            # Sales permissions
            {'name': 'view_sales', 'description': 'Can view sales records', 'category': 'Sales'},
            {'name': 'add_sales', 'description': 'Can create new sales', 'category': 'Sales'},
            {'name': 'edit_sales', 'description': 'Can edit existing sales', 'category': 'Sales'},
            {'name': 'delete_sales', 'description': 'Can delete sales records', 'category': 'Sales'},
            {'name': 'process_pos_sales', 'description': 'Can process point of sale transactions', 'category': 'Sales'},
            
            # Purchase permissions
            {'name': 'view_purchases', 'description': 'Can view purchase records', 'category': 'Purchases'},
            {'name': 'add_purchases', 'description': 'Can create new purchases', 'category': 'Purchases'},
            {'name': 'edit_purchases', 'description': 'Can edit existing purchases', 'category': 'Purchases'},
            {'name': 'delete_purchases', 'description': 'Can delete purchase records', 'category': 'Purchases'},
            
            # Customer permissions
            {'name': 'view_customers', 'description': 'Can view customer records', 'category': 'Customers'},
            {'name': 'add_customers', 'description': 'Can add new customers', 'category': 'Customers'},
            {'name': 'edit_customers', 'description': 'Can edit existing customers', 'category': 'Customers'},
            {'name': 'delete_customers', 'description': 'Can delete customers', 'category': 'Customers'},
            
            # Supplier permissions
            {'name': 'view_suppliers', 'description': 'Can view supplier records', 'category': 'Suppliers'},
            {'name': 'add_suppliers', 'description': 'Can add new suppliers', 'category': 'Suppliers'},
            {'name': 'edit_suppliers', 'description': 'Can edit existing suppliers', 'category': 'Suppliers'},
            {'name': 'delete_suppliers', 'description': 'Can delete suppliers', 'category': 'Suppliers'},
            
            # Expense permissions
            {'name': 'view_expenses', 'description': 'Can view expense records', 'category': 'Expenses'},
            {'name': 'add_expenses', 'description': 'Can add new expenses', 'category': 'Expenses'},
            {'name': 'edit_expenses', 'description': 'Can edit existing expenses', 'category': 'Expenses'},
            {'name': 'delete_expenses', 'description': 'Can delete expenses', 'category': 'Expenses'},
            
            # Report permissions
            {'name': 'view_reports', 'description': 'Can view system reports', 'category': 'Reports'},
            {'name': 'export_reports', 'description': 'Can export reports', 'category': 'Reports'},
            
            # User management permissions
            {'name': 'view_users', 'description': 'Can view user accounts', 'category': 'Users'},
            {'name': 'add_users', 'description': 'Can create new user accounts', 'category': 'Users'},
            {'name': 'edit_users', 'description': 'Can edit user accounts', 'category': 'Users'},
            {'name': 'delete_users', 'description': 'Can delete user accounts', 'category': 'Users'},
            {'name': 'assign_permissions', 'description': 'Can assign permissions to users', 'category': 'Users'},
            
            # Settings permissions
            {'name': 'view_settings', 'description': 'Can view system settings', 'category': 'Settings'},
            {'name': 'edit_settings', 'description': 'Can modify system settings', 'category': 'Settings'},
        ]
        
        # Create permissions
        created_count = 0
        for perm_data in default_permissions:
            perm, created = Permission.objects.get_or_create(
                name=perm_data['name'],
                defaults={
                    'description': perm_data['description'],
                    'category': perm_data['category']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created permission: {perm.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} permissions')
        )