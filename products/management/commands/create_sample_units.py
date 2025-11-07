from django.core.management.base import BaseCommand
from superadmin.models import Business
from products.models import Unit

class Command(BaseCommand):
    help = 'Create sample units for the first business'

    def handle(self, *args, **options):
        # Get the first business
        business = Business.objects.first()
        
        if not business:
            self.stdout.write(
                self.style.ERROR('No business found!')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(f'Creating units for business: {business.company_name}')
        )
        
        # Sample units data
        units_data = [
            {'name': 'Piece', 'symbol': 'pc'},
            {'name': 'Kilogram', 'symbol': 'kg'},
            {'name': 'Liter', 'symbol': 'L'},
            {'name': 'Meter', 'symbol': 'm'},
            {'name': 'Box', 'symbol': 'box'},
            {'name': 'Pack', 'symbol': 'pack'}
        ]
        
        created_count = 0
        
        for unit_data in units_data:
            unit, created = Unit.objects.get_or_create(
                business=business,
                name=unit_data['name'],
                defaults={'symbol': unit_data['symbol']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created unit: {unit.name} ({unit.symbol})')
                )
                created_count += 1
            else:
                self.stdout.write(
                    f'Unit already exists: {unit.name} ({unit.symbol})'
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new units')
        )