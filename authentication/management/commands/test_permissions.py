from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):
    help = 'Test the permission system'

    def handle(self, *args, **options):
        # Create a test user if one doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'role': 'cashier'
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write('Created test user: testuser')
        else:
            self.stdout.write('Using existing test user: testuser')
        
        # Test permission checking
        self.stdout.write(f'User has view_products permission: {user.has_custom_permission("view_products")}')
        self.stdout.write(f'User has add_products permission: {user.has_custom_permission("add_products")}')
        self.stdout.write(f'User has edit_products permission: {user.has_custom_permission("edit_products")}')
        
        self.stdout.write(
            self.style.SUCCESS('Permission system test completed')
        )