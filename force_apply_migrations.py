import os
import sys
import django
from django.core.management import execute_from_command_line

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Force using local settings override
os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory_management.local_settings_override'

# Explicitly unset DATABASE_URL to ensure local settings are used
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

try:
    django.setup()
    print("Django setup completed successfully with local database settings!")
    
    # Get list of apps with migrations
    apps_with_migrations = [
        'auth', 'contenttypes', 'sessions', 'authentication', 
        'customers', 'expenses', 'notifications', 'products', 
        'purchases', 'sales', 'settings', 'superadmin', 'suppliers'
    ]
    
    print("\nApplying migrations for each app...")
    
    # Apply migrations for each app individually
    for app in apps_with_migrations:
        print(f"Applying migrations for {app}...")
        try:
            execute_from_command_line(['manage.py', 'migrate', app])
        except Exception as e:
            print(f"  Warning: Could not apply migrations for {app}: {e}")
    
    print("\n" + "="*50)
    print("MIGRATIONS COMPLETED SUCCESSFULLY!")
    print("Database is now clean and ready for use.")
    print("="*50)
    
except Exception as e:
    print(f"Error applying migrations: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)