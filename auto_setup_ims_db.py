#!/usr/bin/env python3
"""
Automatic setup script for PostgreSQL IMS database.
This script automatically creates the database, tables, and verifies the setup.
"""

import psycopg2
import sys
import os
from psycopg2 import sql

def connect_as_superuser():
    """Connect to PostgreSQL as superuser to create database."""
    try:
        conn = psycopg2.connect(
            dbname='postgres',  # Connect to default postgres database
            user='postgres',
            password='Jesuslove@12',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True  # Enable autocommit for database creation
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting as superuser: {e}")
        return None

def create_database():
    """Create the inventory_db database."""
    conn = connect_as_superuser()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Terminate existing connections to the database if any
        cursor.execute("""
            SELECT pg_terminate_backend(pid) 
            FROM pg_stat_activity 
            WHERE datname = 'ims_db' AND pid <> pg_backend_pid()
        """)
        
        # Drop database if it exists
        cursor.execute("DROP DATABASE IF EXISTS ims_db")
        
        # Create the database
        cursor.execute("CREATE DATABASE ims_db")
        
        print("✓ Database 'ims_db' created successfully")
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        return False

def create_tables():
    """Create all required tables in the ims_db database."""
    try:
        conn = psycopg2.connect(
            dbname='ims_db',
            user='postgres',
            password='Jesuslove@12',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        
        # Create the tenants table
        cursor.execute("""
            CREATE TABLE tenants (
                tenant_id SERIAL PRIMARY KEY,
                business_name VARCHAR(255) NOT NULL,
                contact_email VARCHAR(255) UNIQUE NOT NULL,
                contact_phone VARCHAR(20),
                address TEXT,
                subscription_plan VARCHAR(50) NOT NULL DEFAULT 'basic',
                status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✓ Tenants table created successfully")
        
        # Create the users table
        cursor.execute("""
            CREATE TABLE users (
                user_id SERIAL PRIMARY KEY,
                tenant_id INTEGER NOT NULL,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'manager', 'user')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
            )
        """)
        
        print("✓ Users table created successfully")
        
        # Create the products table
        cursor.execute("""
            CREATE TABLE products (
                product_id SERIAL PRIMARY KEY,
                tenant_id INTEGER NOT NULL,
                product_name VARCHAR(255) NOT NULL,
                sku VARCHAR(100) UNIQUE NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                buying_price DECIMAL(10, 2) NOT NULL,
                selling_price DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
            )
        """)
        
        print("✓ Products table created successfully")
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX idx_users_tenant_id ON users(tenant_id)")
        cursor.execute("CREATE INDEX idx_products_tenant_id ON products(tenant_id)")
        cursor.execute("CREATE INDEX idx_tenants_status ON tenants(status)")
        
        print("✓ Indexes created successfully")
        
        # Commit changes
        conn.commit()
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("✓ All tables and indexes created successfully")
        return True
        
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
        return False

def verify_setup():
    """Verify that the database and tables are properly set up."""
    try:
        conn = psycopg2.connect(
            dbname='ims_db',
            user='postgres',
            password='Jesuslove@12',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        
        # Check if tables exist
        tables = ['tenants', 'users', 'products']
        for table in tables:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                )
            """, (table,))
            
            exists = cursor.fetchone()[0]
            if exists:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' does not exist")
                return False
        
        # Test inserting sample data
        cursor.execute("""
            INSERT INTO tenants (business_name, contact_email, subscription_plan)
            VALUES (%s, %s, %s)
            RETURNING tenant_id
        """, ('Test Company', 'test@company.com', 'basic'))
        
        tenant_id = cursor.fetchone()[0]
        print(f"✓ Sample tenant inserted with ID: {tenant_id}")
        
        cursor.execute("""
            INSERT INTO users (tenant_id, name, email, password_hash, role)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING user_id
        """, (tenant_id, 'Test User', 'test@user.com', 'test_hash', 'admin'))
        
        user_id = cursor.fetchone()[0]
        print(f"✓ Sample user inserted with ID: {user_id}")
        
        cursor.execute("""
            INSERT INTO products (tenant_id, product_name, sku, quantity, buying_price, selling_price)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING product_id
        """, (tenant_id, 'Test Product', 'TEST-001', 10, 5.00, 10.00))
        
        product_id = cursor.fetchone()[0]
        print(f"✓ Sample product inserted with ID: {product_id}")
        
        # Test querying data
        cursor.execute("SELECT COUNT(*) FROM tenants")
        tenant_count = cursor.fetchone()[0]
        print(f"✓ Tenants table contains {tenant_count} record(s)")
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"✓ Users table contains {user_count} record(s)")
        
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        print(f"✓ Products table contains {product_count} record(s)")
        
        # Clean up test data
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM tenants WHERE tenant_id = %s", (tenant_id,))
        
        # Commit changes
        conn.commit()
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("✓ Database setup verification completed successfully")
        return True
        
    except psycopg2.Error as e:
        print(f"Error verifying setup: {e}")
        return False

def main():
    """Main function to automatically set up the IMS database."""
    print("Starting automatic setup of PostgreSQL IMS database...")
    print("=" * 50)
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    if not create_database():
        print("✗ Failed to create database")
        sys.exit(1)
    
    # Step 2: Create tables
    print("\nStep 2: Creating tables...")
    if not create_tables():
        print("✗ Failed to create tables")
        sys.exit(1)
    
    # Step 3: Verify setup
    print("\nStep 3: Verifying setup...")
    if not verify_setup():
        print("✗ Failed to verify setup")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✓ Automatic database setup completed successfully!")
    print("\nThe following components have been created:")
    print("  - Database: ims_db")
    print("  - Tables: tenants, users, products")
    print("  - Indexes: tenant_id indexes for performance")
    print("  - Constraints: Primary keys, foreign keys, unique constraints, check constraints")
    print("\nDatabase is ready for use with the Inventory Management System.")

if __name__ == "__main__":
    main()