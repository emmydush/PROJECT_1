#!/usr/bin/env python
"""
Render Deployment Setup Script

This script is designed to be run during Render deployment to:
1. Create initial migrations
2. Apply migrations to set up the database schema
3. Create a default superuser if none exists
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_render_deployment():
    """Setup the application for Render deployment"""
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
    
    try:
        django.setup()
        print("Django setup completed successfully!")
        
        # Create migrations
        print("\nCreating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Apply migrations
        print("\nApplying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Create superuser if it doesn't exist
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            print("\nCreating default superuser...")
            User.objects.create_superuser(
                username='admin',
                email='admin@inventorysystem.com',
                password='admin123',
                role='admin'
            )
            print("Default superuser created!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("\nSuperuser already exists.")
        
        print("\n" + "="*50)
        print("RENDER DEPLOYMENT SETUP COMPLETED SUCCESSFULLY!")
        print("="*50)
        
    except Exception as e:
        print(f"Error during Render deployment setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    setup_render_deployment()