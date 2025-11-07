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

def check_business():
    try:
        business = Business.objects.get(id=1)
        print(f"Business with ID 1: {business.company_name}")
    except Business.DoesNotExist:
        print("Business with ID 1 does not exist")

if __name__ == "__main__":
    check_business()