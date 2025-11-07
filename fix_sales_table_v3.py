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
        
        # 1. Add the missing payment_method column
        print("1. Adding missing payment_method column...")
        cursor.execute("""
            ALTER TABLE sales_sale 
            ADD COLUMN IF NOT EXISTS payment_method VARCHAR(20) DEFAULT 'cash';
        """)
        
        # 2. Check if payment_status exists and migrate data if needed
        print("2. Checking if payment_status column exists...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'sales_sale' AND column_name = 'payment_status';
        """)
        
        payment_status_exists = cursor.fetchone()
        
        if payment_status_exists:
            print("   Found payment_status column. Migrating data to payment_method...")
            # Map payment_status values to payment_method values
            # This is a simple mapping - you may need to adjust based on your actual data
            cursor.execute("""
                UPDATE sales_sale 
                SET payment_method = CASE 
                    WHEN payment_status = 'paid' THEN 'cash'
                    WHEN payment_status = 'pending' THEN 'cash'
                    WHEN payment_status = 'cancelled' THEN 'cash'
                    ELSE 'cash'
                END
                WHERE payment_method = 'cash' OR payment_method IS NULL;
            """)
            
            # Drop the old payment_status column
            print("   Dropping old payment_status column...")
            cursor.execute("""
                ALTER TABLE sales_sale 
                DROP COLUMN IF EXISTS payment_status;
            """)
        else:
            print("   payment_status column not found, skipping data migration...")
        
        # 3. Add the missing notes column
        print("3. Adding missing notes column...")
        cursor.execute("""
            ALTER TABLE sales_sale 
            ADD COLUMN IF NOT EXISTS notes TEXT NULL;
        """)
        
        # 4. Add the missing is_refunded column
        print("4. Adding missing is_refunded column...")
        cursor.execute("""
            ALTER TABLE sales_sale 
            ADD COLUMN IF NOT EXISTS is_refunded BOOLEAN DEFAULT FALSE;
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