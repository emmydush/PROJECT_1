import psycopg2
import sys
from psycopg2 import sql

def check_sales_columns_detailed():
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
        print("-" * 70)
        for column in columns:
            print(f"Column: {column[0]:20} | Type: {column[1]:15} | Nullable: {column[2]:5} | Default: {column[3]}")
        
        # Check for specific columns
        column_names = [col[0] for col in columns]
        required_columns = ['subtotal', 'tax', 'discount', 'total_amount']
        missing_columns = [col for col in required_columns if col not in column_names]
        
        print(f"\nMissing columns: {missing_columns}")
        
        # Check if old column names exist
        old_columns = ['discount_amount', 'tax_amount']
        existing_old_columns = [col for col in old_columns if col in column_names]
        print(f"Old columns that need renaming: {existing_old_columns}")
        
        cursor.close()
        conn.close()
        
        return column_names, missing_columns, existing_old_columns
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_sales_columns_detailed()