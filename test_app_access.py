import os
import sys
import django
from django.test import Client
from django.urls import reverse

# Force using local settings override
os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory_management.local_settings_override'

# Explicitly unset DATABASE_URL to ensure local settings are used
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

try:
    django.setup()
    
    # Create a test client
    client = Client()
    
    # Test accessing the main page
    print("Testing access to main page...")
    response = client.get('/')
    print(f"Main page response status: {response.status_code}")
    
    # Test accessing the admin page
    print("Testing access to admin page...")
    response = client.get('/admin/')
    print(f"Admin page response status: {response.status_code}")
    
    # Test accessing the login page
    print("Testing access to login page...")
    response = client.get('/accounts/login/')
    print(f"Login page response status: {response.status_code}")
    
    print("Application access test completed!")
    
except Exception as e:
    print(f"Error testing application access: {e}")
    import traceback
    traceback.print_exc()