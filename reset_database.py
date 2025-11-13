import os
import sys
import django
import psycopg2
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

def reset_database():
    """Reset the database by dropping and recreating it"""
    try:
        # Connect to PostgreSQL server (not to the specific database)
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Jesuslove@12",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Terminate all connections to the database
        cursor.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'ims_db'
            AND pid <> pg_backend_pid();
        """)
        
        # Drop the database if it exists
        cursor.execute("DROP DATABASE IF EXISTS ims_db")
        print("Dropped existing database")
        
        # Create a new database
        cursor.execute("CREATE DATABASE ims_db")
        print("Created new database")
        
        # Close connections
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error resetting database: {e}")
        return False

def reset_migrations():
    """Remove all migration files"""
    try:
        # List of apps with migrations
        apps_with_migrations = [
            'authentication', 'customers', 'dashboard', 'expenses', 
            'notifications', 'products', 'purchases', 'reports', 
            'sales', 'settings', 'superadmin', 'suppliers'
        ]
        
        for app in apps_with_migrations:
            migrations_path = os.path.join(os.path.dirname(__file__), app, 'migrations')
            if os.path.exists(migrations_path):
                for file in os.listdir(migrations_path):
                    if file.endswith('.py') and file != '__init__.py':
                        file_path = os.path.join(migrations_path, file)
                        os.remove(file_path)
                        print(f"Removed migration file: {file_path}")
        
        print("All migration files removed")
        return True
    except Exception as e:
        print(f"Error removing migration files: {e}")
        return False

if __name__ == "__main__":
    print("Resetting database and migrations...")
    
    # Reset database
    if reset_database():
        print("Database reset successfully")
    else:
        print("Failed to reset database")
        sys.exit(1)
    
    # Reset migrations
    if reset_migrations():
        print("Migrations reset successfully")
    else:
        print("Failed to reset migrations")
        sys.exit(1)
    
    print("\nDatabase and migrations have been completely reset!")
    print("You can now run migrations to set up a clean database.")