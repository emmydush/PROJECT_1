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
    
    # Check what tables exist
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    
    print("Database tables:")
    for table in tables:
        # Get row count for each table
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]} ({count} rows)")
    
    # Check migration status
    cursor.execute("SELECT COUNT(*) FROM django_migrations;")
    migration_count = cursor.fetchone()[0]
    print(f"\nTotal migrations applied: {migration_count}")
    
    # Close connection
    cursor.close()
    connection.close()
    
    print("\nDatabase verification complete!")
    
except Exception as e:
    print(f"Error verifying database: {e}")
    import traceback
    traceback.print_exc()