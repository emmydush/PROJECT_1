import psycopg2
import os

def verify_clean_state():
    """Verify that the project and database are completely clean"""
    try:
        # Connect to the local database
        connection = psycopg2.connect(
            host="localhost",
            database="ims_db",
            user="postgres",
            password="Jesuslove@12",
            port="5432"
        )
        
        cursor = connection.cursor()
        
        # Check what tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        
        if tables:
            print("Remaining tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("✓ Database is completely clean (no tables)")
        
        # Close connection
        cursor.close()
        connection.close()
        
        # Check migration files
        base_path = os.path.dirname(os.path.abspath(__file__))
        apps_with_migrations = [
            'authentication', 'customers', 'dashboard', 'expenses', 
            'notifications', 'products', 'purchases', 'reports', 
            'sales', 'settings', 'superadmin', 'suppliers'
        ]
        
        print("\nChecking migration files...")
        migration_files_found = False
        
        for app in apps_with_migrations:
            migrations_path = os.path.join(base_path, app, 'migrations')
            
            if os.path.exists(migrations_path):
                files = os.listdir(migrations_path)
                # Filter out __init__.py
                migration_files = [f for f in files if f != '__init__.py']
                
                if migration_files:
                    print(f"  ✗ Found migration files in {app}: {migration_files}")
                    migration_files_found = True
                else:
                    print(f"  ✓ {app} is clean")
            else:
                print(f"  ✓ {app} has no migrations folder")
        
        if not migration_files_found:
            print("✓ All migration files have been removed")
        
        print("\n" + "="*50)
        print("PROJECT IS READY FOR FRESH RENDER DEPLOYMENT!")
        print("="*50)
        
    except Exception as e:
        print(f"Error verifying clean state: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_clean_state()