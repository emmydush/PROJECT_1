import os
import sys
import django
from django.db import connection

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
    
    # Check existing constraints on products_product table
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT constraint_name, constraint_type 
            FROM information_schema.table_constraints 
            WHERE table_name = 'products_product' 
            AND constraint_type = 'UNIQUE'
            ORDER BY constraint_name;
        """)
        constraints = cursor.fetchall()
        
        print("Current unique constraints on products_product table:")
        for constraint in constraints:
            print(f"  - {constraint[0]} ({constraint[1]})")
            
        # Check specifically for constraints involving sku
        cursor.execute("""
            SELECT constraint_name 
            FROM information_schema.constraint_column_usage 
            WHERE table_name = 'products_product' 
            AND column_name = 'sku';
        """)
        sku_constraints = cursor.fetchall()
        
        print("\nConstraints involving 'sku' column:")
        for constraint in sku_constraints:
            print(f"  - {constraint[0]}")
            
except Exception as e:
    print(f"Error checking constraints: {e}")
    import traceback
    traceback.print_exc()