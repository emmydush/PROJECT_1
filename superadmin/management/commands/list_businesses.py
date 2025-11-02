from django.core.management.base import BaseCommand
from superadmin.models import Business
from authentication.models import User

class Command(BaseCommand):
    help = 'List all businesses and their owners'

    def handle(self, *args, **options):
        businesses = Business.objects.all()
        
        if not businesses:
            self.stdout.write('No businesses found')
            return
            
        self.stdout.write('Businesses and their owners:')
        self.stdout.write('=' * 60)
        
        for business in businesses:
            owner_username = business.owner.username if business.owner else 'No Owner'
            owner_email = business.owner.email if business.owner else 'No Email'
            self.stdout.write(f'{business.company_name:<25} | {owner_username:<20} | {owner_email}')
            
        self.stdout.write('=' * 60)
        self.stdout.write(f'Total businesses: {len(businesses)}')