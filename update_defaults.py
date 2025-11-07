#!/usr/bin/env python3
"""
Script to update default values in the settings_businesssettings table.
"""

import psycopg2

def update_defaults():
    """Update default values in the settings_businesssettings table."""
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
        
        # Update default values
        cursor.execute("UPDATE settings_businesssettings SET business_name = 'Smart Solution' WHERE business_name IS NULL")
        cursor.execute("UPDATE settings_businesssettings SET business_address = '123 Business Street, City, Country' WHERE business_address IS NULL")
        cursor.execute("UPDATE settings_businesssettings SET business_email = 'info@smartsolution.com' WHERE business_email IS NULL")
        cursor.execute("UPDATE settings_businesssettings SET business_phone = '+1 (555) 123-4567' WHERE business_phone IS NULL")
        cursor.execute("UPDATE settings_businesssettings SET currency = 'FRW' WHERE currency IS NULL")
        cursor.execute("UPDATE settings_businesssettings SET currency_symbol = 'FRW' WHERE currency_symbol IS NULL")
        cursor.execute("UPDATE settings_businesssettings SET tax_rate = 0 WHERE tax_rate IS NULL")
        
        # Commit changes
        conn.commit()
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("Updated default values in settings_businesssettings table")
        return True
        
    except psycopg2.Error as e:
        print(f"Error updating default values: {e}")
        return False

if __name__ == "__main__":
    update_defaults()