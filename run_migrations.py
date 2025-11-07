import os
import sys
import django
from django.core.management import execute_from_command_line

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

try:
    django.setup()
    print("Django setup completed successfully!")
    
    # Show migration status
    print("\nChecking migration status...")
    execute_from_command_line(['manage.py', 'showmigrations'])
    
    # Apply migrations
    print("\nApplying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("\n" + "="*50)
    print("MIGRATIONS COMPLETED SUCCESSFULLY!")
    print("="*50)
    
except Exception as e:
    print(f"Error during migration process: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)