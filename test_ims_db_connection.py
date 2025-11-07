#!/usr/bin/env python3
"""
Test connection to the PostgreSQL IMS database.
This script tests the connection to the newly created IMS database.
"""

import psycopg2
from psycopg2 import sql

def test_database_connection():
    """Test connection to the PostgreSQL IMS database."""
    try:
        # Database connection parameters
        conn_params = {
            'dbname': 'ims_db',
            'user': 'postgres',
            'password': 'Jesuslove@12',
            'host': 'localhost',
            'port': '5432'
        }
        
        # Establish connection
        print("Attempting to connect to PostgreSQL IMS database...")
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Execute a simple query to test the connection
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"PostgreSQL version: {db_version[0]}")
        
        # Test that our tables exist
        tables = ['tenants', 'users', 'products']
        for table in tables:
            cursor.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table)))
            count = cursor.fetchone()[0]
            print(f"Table '{table}' exists with {count} rows")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("Connected successfully to PostgreSQL IMS database")
        return True
        
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def insert_sample_data():
    """Insert sample data to verify functionality."""
    try:
        # Database connection parameters
        conn_params = {
            'dbname': 'ims_db',
            'user': 'postgres',
            'password': 'Jesuslove@12',
            'host': 'localhost',
            'port': '5432'
        }
        
        # Establish connection
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Insert sample tenant
        cursor.execute("""
            INSERT INTO tenants (business_name, contact_email, contact_phone, address, subscription_plan)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING tenant_id
        """, ('Tech Solutions Inc.', 'contact@techsolutions.com', '+1234567890', '123 Tech Street, Silicon Valley', 'premium'))
        
        tenant_id = cursor.fetchone()[0]
        print(f"Inserted tenant with ID: {tenant_id}")
        
        # Insert sample user
        cursor.execute("""
            INSERT INTO users (tenant_id, name, email, password_hash, role)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING user_id
        """, (tenant_id, 'John Doe', 'john.doe@techsolutions.com', 'hashed_password_123', 'admin'))
        
        user_id = cursor.fetchone()[0]
        print(f"Inserted user with ID: {user_id}")
        
        # Insert sample products
        products_data = [
            (tenant_id, 'Laptop Model X', 'LAPTOP-X-001', 50, 800.00, 1200.00),
            (tenant_id, 'Wireless Mouse Pro', 'MOUSE-P-002', 200, 15.00, 35.00),
            (tenant_id, 'USB-C Hub', 'HUB-C-003', 75, 25.00, 45.00)
        ]
        
        for product_data in products_data:
            cursor.execute("""
                INSERT INTO products (tenant_id, product_name, sku, quantity, buying_price, selling_price)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING product_id
            """, product_data)
            
            product_id = cursor.fetchone()[0]
            print(f"Inserted product with ID: {product_id}")
        
        # Commit changes
        conn.commit()
        
        # Retrieve and display data
        print("\n--- Sample Data Verification ---")
        
        # Retrieve tenant
        cursor.execute("SELECT * FROM tenants WHERE tenant_id = %s", (tenant_id,))
        tenant = cursor.fetchone()
        print(f"Tenant: {tenant}")
        
        # Retrieve user
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        print(f"User: {user}")
        
        # Retrieve products
        cursor.execute("SELECT * FROM products WHERE tenant_id = %s", (tenant_id,))
        products = cursor.fetchall()
        print(f"Products: {products}")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\nSample data inserted and verified successfully!")
        return True
        
    except psycopg2.Error as e:
        print(f"Error inserting sample data: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def test_tenant_isolation():
    """Test tenant isolation by creating multiple tenants and verifying data separation."""
    try:
        # Database connection parameters
        conn_params = {
            'dbname': 'ims_db',
            'user': 'postgres',
            'password': 'Jesuslove@12',
            'host': 'localhost',
            'port': '5432'
        }
        
        # Establish connection
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Insert second tenant
        cursor.execute("""
            INSERT INTO tenants (business_name, contact_email, contact_phone, address, subscription_plan)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING tenant_id
        """, ('Global Retail Corp.', 'info@globalretail.com', '+0987654321', '456 Retail Ave, Business District', 'basic'))
        
        tenant2_id = cursor.fetchone()[0]
        print(f"Inserted second tenant with ID: {tenant2_id}")
        
        # Insert products for second tenant
        products_data_t2 = [
            (tenant2_id, 'Office Chair Deluxe', 'CHAIR-D-001', 30, 75.00, 150.00),
            (tenant2_id, 'Desk Lamp LED', 'LAMP-L-002', 100, 20.00, 45.00)
        ]
        
        for product_data in products_data_t2:
            cursor.execute("""
                INSERT INTO products (tenant_id, product_name, sku, quantity, buying_price, selling_price)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING product_id
            """, product_data)
            
            product_id = cursor.fetchone()[0]
            print(f"Inserted product for tenant 2 with ID: {product_id}")
        
        # Commit changes
        conn.commit()
        
        # Test tenant isolation - each tenant should only see their own data
        print("\n--- Tenant Isolation Test ---")
        
        # Fetch products for tenant 1
        cursor.execute("SELECT product_name FROM products WHERE tenant_id = %s", (1,))
        tenant1_products = cursor.fetchall()
        print(f"Tenant 1 products: {[p[0] for p in tenant1_products]}")
        
        # Fetch products for tenant 2
        cursor.execute("SELECT product_name FROM products WHERE tenant_id = %s", (tenant2_id,))
        tenant2_products = cursor.fetchall()
        print(f"Tenant 2 products: {[p[0] for p in tenant2_products]}")
        
        # Verify isolation - tenant 1 should not see tenant 2's products
        all_product_names_t1 = [p[0] for p in tenant1_products]
        all_product_names_t2 = [p[0] for p in tenant2_products]
        
        # Check that there's no overlap
        overlap = set(all_product_names_t1).intersection(set(all_product_names_t2))
        if len(overlap) == 0:
            print("✓ Tenant isolation verified - no data overlap between tenants")
        else:
            print(f"✗ Tenant isolation failed - overlapping products: {overlap}")
        
        # Close connection
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"Error in tenant isolation test: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Testing PostgreSQL IMS Database Connection...\n")
    
    # Test basic connection
    if test_database_connection():
        print("\n" + "="*50)
        
        # Insert sample data
        print("Inserting sample data...")
        if insert_sample_data():
            print("\n" + "="*50)
            
            # Test tenant isolation
            print("Testing tenant isolation...")
            test_tenant_isolation()
    else:
        print("Failed to connect to the database.")