import psycopg2
import sys

def fix_sales_table():
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
        
        # Add missing columns
        print("Adding missing columns...")
        cursor.execute("ALTER TABLE sales_sale ADD COLUMN IF NOT EXISTS subtotal DECIMAL(10,2) DEFAULT 0;")
        cursor.execute("ALTER TABLE sales_sale ADD COLUMN IF NOT EXISTS tax DECIMAL(10,2) DEFAULT 0;")
        cursor.execute("ALTER TABLE sales_sale ADD COLUMN IF NOT EXISTS discount DECIMAL(10,2) DEFAULT 0;")
        
        # Rename existing columns to match Django model
        print("Renaming columns...")
        cursor.execute("ALTER TABLE sales_sale RENAME COLUMN discount_amount TO discount;")
        cursor.execute("ALTER TABLE sales_sale RENAME COLUMN tax_amount TO tax;")
        
        # Update default values for renamed columns
        print("Updating default values...")
        cursor.execute("ALTER TABLE sales_sale ALTER COLUMN discount SET DEFAULT 0;")
        cursor.execute("ALTER TABLE sales_sale ALTER COLUMN tax SET DEFAULT 0;")
        
        # Commit changes
        conn.commit()
        print("Successfully updated sales_sale table!")
        
        # Verify the changes
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'sales_sale'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\nUpdated columns in sales_sale table:")
        print("-" * 50)
        for column in columns:
            print(f"Column: {column[0]}, Type: {column[1]}, Nullable: {column[2]}, Default: {column[3]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_sales_table()