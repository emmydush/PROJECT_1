import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:\\AI')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

# Setup Django
django.setup()

from products.models import Unit
from superadmin.models import Business
from superadmin.middleware import set_current_business, get_current_business

def test_manager():
    # Get the business
    business = Business.objects.get(id=1)
    print(f"Testing with business: {business.company_name}")
    
    # Set the current business in thread-local storage
    set_current_business(business)
    
    # Check if it's set
    current = get_current_business()
    print(f"Current business in context: {current.company_name if current else None}")
    
    # Test the business-specific manager
    all_units = Unit.objects.all()
    business_units = Unit.objects.business_specific()
    
    print(f"Total units in DB: {all_units.count()}")
    print(f"Business-specific units: {business_units.count()}")
    
    print("\nAll units:")
    for unit in all_units:
        print(f"  - {unit.name} ({unit.symbol}) - Business: {unit.business.id if unit.business else None}")
    
    print("\nBusiness-specific units:")
    for unit in business_units:
        print(f"  - {unit.name} ({unit.symbol})")

if __name__ == "__main__":
    test_manager()