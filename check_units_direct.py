import psycopg2

def check_units():
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
        
        # Check if units table exists and get its structure
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'products_unit';
        """)
        
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("Units table does not exist")
            return
            
        print("Units table exists")
        
        # Get column information
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'products_unit'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\nTable structure:")
        for column in columns:
            print(f"  {column[0]} ({column[1]}, {'NULL' if column[2] == 'YES' else 'NOT NULL'})")
        
        # Count units
        cursor.execute("SELECT COUNT(*) FROM products_unit;")
        count = cursor.fetchone()[0]
        print(f"\nTotal units: {count}")
        
        # Get sample units
        if count > 0:
            cursor.execute("SELECT id, name, symbol, business_id FROM products_unit LIMIT 5;")
            units = cursor.fetchall()
            print("\nSample units:")
            for unit in units:
                print(f"  ID: {unit[0]}, Name: {unit[1]}, Symbol: {unit[2]}, Business ID: {unit[3]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_units()