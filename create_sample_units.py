import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:\\AI')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

# Setup Django
django.setup()

from superadmin.models import Business
from products.models import Unit

def create_sample_units():
    # Get the first business
    business = Business.objects.first()
    
    if not business:
        print("No business found!")
        return
    
    print(f"Creating units for business: {business.company_name}")
    
    # Sample units data
    units_data = [
        {'name': 'Piece', 'symbol': 'pc'},
        {'name': 'Kilogram', 'symbol': 'kg'},
        {'name': 'Liter', 'symbol': 'L'},
        {'name': 'Meter', 'symbol': 'm'},
        {'name': 'Box', 'symbol': 'box'},
        {'name': 'Pack', 'symbol': 'pack'}
    ]
    
    created_units = []
    
    for unit_data in units_data:
        unit, created = Unit.objects.get_or_create(
            business=business,
            name=unit_data['name'],
            defaults={'symbol': unit_data['symbol']}
        )
        created_units.append((unit.name, created))
        if created:
            print(f"Created unit: {unit.name} ({unit.symbol})")
        else:
            print(f"Unit already exists: {unit.name} ({unit.symbol})")
    
    print(f"Total units created/already existing: {len(created_units)}")

if __name__ == "__main__":
    # Run the function
    create_sample_units()