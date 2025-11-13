import psycopg2
import os

def clean_database():
    """Clean the database for fresh Render deployment"""
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
        
        # Drop all tables except the Django-specific ones that might be needed
        cursor.execute("""
            DO $$ 
            DECLARE 
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)
        
        print("All tables dropped successfully!")
        
        # Close connection
        cursor.close()
        connection.close()
        
        print("Database cleaned successfully for Render deployment!")
        
    except Exception as e:
        print(f"Error cleaning database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Cleaning database for fresh Render deployment...")
    clean_database()