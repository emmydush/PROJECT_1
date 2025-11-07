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
        
        print("Fixing sales_sale table to match Django model...")
        
        # 1. Add the missing subtotal column
        print("1. Adding missing subtotal column...")
        cursor.execute("""
            ALTER TABLE sales_sale 
            ADD COLUMN IF NOT EXISTS subtotal DECIMAL(10,2) DEFAULT 0;
        """)
        
        # 2. Rename discount_amount to discount if discount doesn't exist yet
        print("2. Checking if we need to rename discount_amount...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'sales_sale' AND column_name = 'discount';
        """)
        
        discount_exists = cursor.fetchone()
        
        if not discount_exists:
            print("   Renaming discount_amount to discount...")
            cursor.execute("""
                ALTER TABLE sales_sale 
                RENAME COLUMN discount_amount TO discount;
            """)
        else:
            print("   Discount column already exists, skipping rename...")
        
        # 3. Rename tax_amount to tax if tax doesn't exist yet
        print("3. Checking if we need to rename tax_amount...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'sales_sale' AND column_name = 'tax';
        """)
        
        tax_exists = cursor.fetchone()
        
        if not tax_exists:
            print("   Renaming tax_amount to tax...")
            cursor.execute("""
                ALTER TABLE sales_sale 
                RENAME COLUMN tax_amount TO tax;
            """)
        else:
            print("   Tax column already exists, skipping rename...")
        
        # 4. Set default values for the columns
        print("4. Setting default values...")
        cursor.execute("""
            ALTER TABLE sales_sale 
            ALTER COLUMN discount SET DEFAULT 0;
        """)
        
        cursor.execute("""
            ALTER TABLE sales_sale 
            ALTER COLUMN tax SET DEFAULT 0;
        """)
        
        cursor.execute("""
            ALTER TABLE sales_sale 
            ALTER COLUMN subtotal SET DEFAULT 0;
        """)
        
        # 5. Update subtotal values to match existing data
        # Since we don't have the original itemized data, we'll calculate it
        # as total_amount - tax + discount (this is an approximation)
        print("5. Updating subtotal values...")
        cursor.execute("""
            UPDATE sales_sale 
            SET subtotal = COALESCE(total_amount, 0) - COALESCE(tax, 0) + COALESCE(discount, 0)
            WHERE subtotal = 0 OR subtotal IS NULL;
        """)
        
        # Commit changes
        conn.commit()
        print("\nSuccessfully updated sales_sale table!")
        
        # Verify the changes
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'sales_sale'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\nUpdated columns in sales_sale table:")
        print("-" * 70)
        for column in columns:
            print(f"Column: {column[0]:20} | Type: {column[1]:15} | Nullable: {column[2]:5} | Default: {column[3]}")
        
        cursor.close()
        conn.close()
        
        print("\nThe sales_sale table has been successfully updated to match the Django model.")
        print("You can now restart your Django server.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_sales_table()