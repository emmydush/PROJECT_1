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

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

# Explicitly unset DATABASE_URL to ensure local settings are used
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

try:
    django.setup()
    print("Django setup completed successfully!")
    
    # Run the development server
    print("\nStarting development server...")
    execute_from_command_line(['manage.py', 'runserver', '8000'])
    
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)