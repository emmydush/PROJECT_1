import os
import sys
import django

# Force using local settings override
os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory_management.local_settings_override'

# Explicitly unset DATABASE_URL to ensure local settings are used
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

try:
    django.setup()
    
    from django.conf import settings
    
    print("Installed apps:")
    for app in settings.INSTALLED_APPS:
        print(f"  - {app}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()