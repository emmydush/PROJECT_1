import os
import sys
import django
from django.contrib.auth import get_user_model

# Force using local settings override
os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory_management.local_settings_override'

# Explicitly unset DATABASE_URL to ensure local settings are used
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

try:
    django.setup()
    
    User = get_user_model()
    
    # Check if superuser already exists
    if User.objects.filter(username='admin').exists():
        print("Superuser 'admin' already exists")
    else:
        # Create superuser
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        print("Superuser 'admin' created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("You can change this password after logging in.")
    
except Exception as e:
    print(f"Error creating superuser: {e}")
    import traceback
    traceback.print_exc()