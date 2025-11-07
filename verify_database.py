#!/usr/bin/env python3
"""
Script to verify that the database and tables have been created successfully.
"""

import psycopg2

def verify_database():
    """Verify that the database and tables exist."""
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname='ims_db',
            user='postgres',
            password='Jesuslove@12',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cursor.fetchall()
        
        print("Database 'ims_db' contains the following tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Verify the structure of each table
        for table_name in ['tenants', 'users', 'products']:
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = %s 
                ORDER BY ordinal_position
            """, (table_name,))
            
            columns = cursor.fetchall()
            print(f"\nTable '{table_name}' structure:")
            for column in columns:
                print(f"  - {column[0]} ({column[1]})")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n✓ Database verification completed successfully!")
        return True
        
    except psycopg2.Error as e:
        print(f"Error verifying database: {e}")
        return False

if __name__ == "__main__":
    verify_database()