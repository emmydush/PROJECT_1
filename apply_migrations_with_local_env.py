import os
import sys
import django
from django.core.management import execute_from_command_line

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load local environment variables from .env.local if it exists
env_path = os.path.join(os.path.dirname(__file__), '.env.local')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
    print("Loaded local environment variables from .env.local")
else:
    print("Local .env.local file not found, using default settings")

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

# Explicitly unset DATABASE_URL to ensure local settings are used
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

try:
    django.setup()
    print("Django setup completed successfully!")
    
    # Show migration status
    print("\nChecking migration status...")
    execute_from_command_line(['manage.py', 'showmigrations'])
    
    # Ask user if they want to apply migrations
    response = input("\nDo you want to apply pending migrations? (y/N): ")
    if response.lower() in ['y', 'yes']:
        print("\nApplying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("\n" + "="*50)
        print("MIGRATIONS COMPLETED SUCCESSFULLY!")
        print("="*50)
    else:
        print("Migration application cancelled.")
    
except Exception as e:
    print(f"Error during migration process: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)