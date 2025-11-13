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
    
    # Run the development server
    print("\nStarting development server on http://127.0.0.1:8000...")
    execute_from_command_line(['manage.py', 'runserver', '8000'])
    
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)