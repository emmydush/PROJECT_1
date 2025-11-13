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
    
    connection.autocommit = True
    cursor = connection.cursor()
    
    # Create the django_migrations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_migrations (
            id BIGSERIAL PRIMARY KEY,
            app VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            applied TIMESTAMP WITH TIME ZONE NOT NULL
        );
    """)
    
    print("Created django_migrations table")
    
    # Close connection
    cursor.close()
    connection.close()
    
    print("Database initialized successfully")
    
except Exception as e:
    print(f"Error initializing database: {e}")
    import traceback
    traceback.print_exc()