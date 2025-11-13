import os
import shutil

# List of apps with migrations
apps_with_migrations = [
    'authentication',
    'customers',
    'dashboard',
    'expenses',
    'notifications',
    'products',
    'purchases',
    'reports',
    'sales',
    'settings',
    'superadmin',
    'suppliers',
]

def remove_migration_files():
    """Remove all migration files and folders"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    for app in apps_with_migrations:
        migrations_path = os.path.join(base_path, app, 'migrations')
        
        if os.path.exists(migrations_path):
            print(f"Cleaning migrations for {app}...")
            
            # Remove all files in migrations folder except __init__.py
            for file in os.listdir(migrations_path):
                file_path = os.path.join(migrations_path, file)
                
                # Skip __init__.py file
                if file == '__init__.py':
                    continue
                    
                # Remove all other files and folders
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"  Removed file: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"  Removed directory: {file_path}")
            
            print(f"  Completed cleaning for {app}")
        else:
            print(f"No migrations folder found for {app}")
    
    print("\nAll migration files have been removed!")

def verify_clean_state():
    """Verify that no migration files remain"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    print("\nVerifying clean state...")
    
    for app in apps_with_migrations:
        migrations_path = os.path.join(base_path, app, 'migrations')
        
        if os.path.exists(migrations_path):
            files = os.listdir(migrations_path)
            # Filter out __init__.py
            migration_files = [f for f in files if f != '__init__.py']
            
            if migration_files:
                print(f"WARNING: Found migration files in {app}: {migration_files}")
            else:
                print(f"✓ {app} is clean")
        else:
            print(f"✓ {app} has no migrations folder")

if __name__ == "__main__":
    print("Removing all migration files for fresh Render deployment...")
    remove_migration_files()
    verify_clean_state()
    print("\nProject is now clean for fresh Render deployment!")