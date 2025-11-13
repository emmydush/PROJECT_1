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
    
    from django.db import connection
    
    # Test database connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"Database connection successful: {result[0]}")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_name IN ('authentication_user', 'superadmin_business')
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print("Required tables:")
        for table in tables:
            print(f"  - {table[0]}")
            
    print("Database test completed successfully!")
    
except Exception as e:
    print(f"Error testing database connection: {e}")
    import traceback
    traceback.print_exc()