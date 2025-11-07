#!/usr/bin/env python3
"""
Script to check what tables exist in the database.
"""

import psycopg2

def check_tables():
    """Check what tables exist in the database."""
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
        
        print("Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Close connection
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error checking tables: {e}")

if __name__ == "__main__":
    check_tables()