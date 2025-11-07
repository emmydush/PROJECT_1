import psycopg2
import sys
from psycopg2 import sql

def check_sales_columns():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host="localhost",
            database="ims_db",
            user="postgres",
            password="Jesuslove@12",
            port="5432"
        )
        
        cursor = conn.cursor()
        
        # Get column information for sales_sale table
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'sales_sale'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print("Current columns in sales_sale table:")
        print("-" * 50)
        for column in columns:
            print(f"Column: {column[0]}, Type: {column[1]}, Nullable: {column[2]}, Default: {column[3]}")
        
        # Check if subtotal column exists
        subtotal_exists = any(column[0] == 'subtotal' for column in columns)
        print(f"\nDoes 'subtotal' column exist? {subtotal_exists}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_sales_columns()