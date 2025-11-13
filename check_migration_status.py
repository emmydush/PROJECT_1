import psycopg2
import os

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
    
    # Check if django_migrations table exists
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'django_migrations';
    """)
    
    result = cursor.fetchone()
    
    if result:
        print("django_migrations table exists")
        
        # Check what migrations have been applied
        cursor.execute("SELECT app, name FROM django_migrations ORDER BY app, name;")
        migrations = cursor.fetchall()
        
        if migrations:
            print("Applied migrations:")
            for app, name in migrations:
                print(f"  - {app}: {name}")
        else:
            print("No migrations have been applied yet")
    else:
        print("django_migrations table does not exist")
    
    # Close connection
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"Error checking migration status: {e}")