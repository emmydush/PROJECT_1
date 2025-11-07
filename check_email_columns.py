#!/usr/bin/env python3
"""
Script to check columns in the settings_emailsettings table.
"""

import psycopg2

def check_email_columns():
    """Check columns in the settings_emailsettings table."""
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
        
        # Get list of columns
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'settings_emailsettings' 
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        
        print("Current columns in settings_emailsettings:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")
        
        # Close connection
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error checking columns: {e}")

if __name__ == "__main__":
    check_email_columns()