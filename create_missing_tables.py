#!/usr/bin/env python3
"""
Script to create any missing tables that Django might need.
"""

import psycopg2

def create_missing_tables():
    """Create any missing tables that Django might need."""
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
        
        # Get list of existing tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        # Tables that Django might need but may be missing
        # We'll check and create them if they don't exist
        
        # Create notifications table if it doesn't exist
        if 'notifications_notification' not in existing_tables:
            cursor.execute("""
                CREATE TABLE notifications_notification (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    notification_type VARCHAR(50) NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER REFERENCES authentication_user(id) ON DELETE CASCADE,
                    business_id INTEGER REFERENCES superadmin_business(id) ON DELETE CASCADE
                )
            """)
            print("✓ Created notifications_notification table")
        
        # Create purchases tables if they don't exist
        if 'purchases_purchaseorder' not in existing_tables:
            cursor.execute("""
                CREATE TABLE purchases_purchaseorder (
                    id SERIAL PRIMARY KEY,
                    order_number VARCHAR(100) UNIQUE NOT NULL,
                    supplier_id INTEGER REFERENCES suppliers_supplier(id) ON DELETE CASCADE,
                    order_date DATE NOT NULL,
                    expected_delivery_date DATE,
                    status VARCHAR(50) DEFAULT 'pending',
                    total_amount DECIMAL(10, 2) DEFAULT 0.00,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    business_id INTEGER REFERENCES superadmin_business(id) ON DELETE CASCADE,
                    created_by_id INTEGER REFERENCES authentication_user(id) ON DELETE SET NULL
                )
            """)
            print("✓ Created purchases_purchaseorder table")
            
        if 'purchases_purchaseitem' not in existing_tables:
            cursor.execute("""
                CREATE TABLE purchases_purchaseitem (
                    id SERIAL PRIMARY KEY,
                    purchase_order_id INTEGER REFERENCES purchases_purchaseorder(id) ON DELETE CASCADE,
                    product_id INTEGER REFERENCES products_product(id) ON DELETE CASCADE,
                    quantity INTEGER NOT NULL CHECK (quantity > 0),
                    unit_price DECIMAL(10, 2) NOT NULL,
                    total_price DECIMAL(10, 2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    business_id INTEGER REFERENCES superadmin_business(id) ON DELETE CASCADE
                )
            """)
            print("✓ Created purchases_purchaseitem table")
        
        # Create sales tables if they don't exist
        if 'sales_sale' not in existing_tables:
            cursor.execute("""
                CREATE TABLE sales_sale (
                    id SERIAL PRIMARY KEY,
                    sale_number VARCHAR(100) UNIQUE NOT NULL,
                    customer_id INTEGER REFERENCES customers_customer(id) ON DELETE SET NULL,
                    sale_date DATE NOT NULL,
                    total_amount DECIMAL(10, 2) DEFAULT 0.00,
                    discount_amount DECIMAL(10, 2) DEFAULT 0.00,
                    tax_amount DECIMAL(10, 2) DEFAULT 0.00,
                    final_amount DECIMAL(10, 2) NOT NULL,
                    payment_status VARCHAR(50) DEFAULT 'pending',
                    sale_type VARCHAR(50) DEFAULT 'regular',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    business_id INTEGER REFERENCES superadmin_business(id) ON DELETE CASCADE,
                    created_by_id INTEGER REFERENCES authentication_user(id) ON DELETE SET NULL
                )
            """)
            print("✓ Created sales_sale table")
            
        if 'sales_saleitem' not in existing_tables:
            cursor.execute("""
                CREATE TABLE sales_saleitem (
                    id SERIAL PRIMARY KEY,
                    sale_id INTEGER REFERENCES sales_sale(id) ON DELETE CASCADE,
                    product_id INTEGER REFERENCES products_product(id) ON DELETE CASCADE,
                    quantity INTEGER NOT NULL CHECK (quantity > 0),
                    unit_price DECIMAL(10, 2) NOT NULL,
                    total_price DECIMAL(10, 2) NOT NULL,
                    discount_amount DECIMAL(10, 2) DEFAULT 0.00,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✓ Created sales_saleitem table")
            
        if 'sales_cart' not in existing_tables:
            cursor.execute("""
                CREATE TABLE sales_cart (
                    id SERIAL PRIMARY KEY,
                    session_key VARCHAR(255),
                    user_id INTEGER REFERENCES authentication_user(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✓ Created sales_cart table")
            
        if 'sales_cartitem' not in existing_tables:
            cursor.execute("""
                CREATE TABLE sales_cartitem (
                    id SERIAL PRIMARY KEY,
                    cart_id INTEGER REFERENCES sales_cart(id) ON DELETE CASCADE,
                    product_id INTEGER REFERENCES products_product(id) ON DELETE CASCADE,
                    quantity INTEGER NOT NULL CHECK (quantity > 0),
                    unit_price DECIMAL(10, 2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (cart_id, product_id)
                )
            """)
            print("✓ Created sales_cartitem table")
            
        if 'sales_refund' not in existing_tables:
            cursor.execute("""
                CREATE TABLE sales_refund (
                    id SERIAL PRIMARY KEY,
                    sale_id INTEGER REFERENCES sales_sale(id) ON DELETE CASCADE,
                    refund_date DATE NOT NULL,
                    reason TEXT,
                    total_amount DECIMAL(10, 2) NOT NULL,
                    status VARCHAR(50) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    business_id INTEGER REFERENCES superadmin_business(id) ON DELETE CASCADE,
                    created_by_id INTEGER REFERENCES authentication_user(id) ON DELETE SET NULL
                )
            """)
            print("✓ Created sales_refund table")
        
        # Create settings tables if they don't exist
        if 'settings_businesssettings' not in existing_tables:
            cursor.execute("""
                CREATE TABLE settings_businesssettings (
                    id SERIAL PRIMARY KEY,
                    business_name VARCHAR(255) NOT NULL,
                    business_address TEXT,
                    business_phone VARCHAR(20),
                    business_email VARCHAR(255),
                    currency VARCHAR(10) DEFAULT 'USD',
                    currency_symbol VARCHAR(5) DEFAULT '$',
                    tax_rate DECIMAL(5, 2) DEFAULT 0.00,
                    timezone VARCHAR(50) DEFAULT 'UTC',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    business_id INTEGER REFERENCES superadmin_business(id) ON DELETE CASCADE
                )
            """)
            print("✓ Created settings_businesssettings table")
            
        if 'settings_emailsettings' not in existing_tables:
            cursor.execute("""
                CREATE TABLE settings_emailsettings (
                    id SERIAL PRIMARY KEY,
                    smtp_host VARCHAR(255),
                    smtp_port INTEGER DEFAULT 587,
                    smtp_username VARCHAR(255),
                    smtp_password VARCHAR(255),
                    use_tls BOOLEAN DEFAULT TRUE,
                    use_ssl BOOLEAN DEFAULT FALSE,
                    default_from_email VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    business_id INTEGER REFERENCES superadmin_business(id) ON DELETE CASCADE
                )
            """)
            print("✓ Created settings_emailsettings table")
            
        if 'settings_backupsettings' not in existing_tables:
            cursor.execute("""
                CREATE TABLE settings_backupsettings (
                    id SERIAL PRIMARY KEY,
                    enable_automatic_backups BOOLEAN DEFAULT FALSE,
                    backup_frequency VARCHAR(20) DEFAULT 'daily',
                    retention_days INTEGER DEFAULT 30,
                    storage_location VARCHAR(255),
                    last_backup TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    business_id INTEGER REFERENCES superadmin_business(id) ON DELETE CASCADE
                )
            """)
            print("✓ Created settings_backupsettings table")
        
        # Commit changes
        conn.commit()
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n✓ Checked and created missing tables as needed")
        return True
        
    except psycopg2.Error as e:
        print(f"Error creating missing tables: {e}")
        return False

if __name__ == "__main__":
    create_missing_tables()