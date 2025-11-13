import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

# Now we can import Django models
from django.db import connection

def check_schema():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'sales_sale' AND table_schema = 'public'")
        columns = cursor.fetchall()
        print("Sales table columns:")
        for column in columns:
            print(f"  {column[0]}: {column[1]}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_schema()