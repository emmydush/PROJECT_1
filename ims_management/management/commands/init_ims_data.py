import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Initialize IMS database with sample data'

    def handle(self, *args, **options):
        # Get database configuration from Django settings
        db_config = settings.DATABASES['default']
        
        # Database connection parameters
        conn_params = {
            'dbname': db_config['NAME'],
            'user': db_config['USER'],
            'password': db_config['PASSWORD'],
            'host': db_config['HOST'],
            'port': db_config['PORT']
        }
        
        try:
            # Establish connection
            conn = psycopg2.connect(**conn_params)
            cursor = conn.cursor()
            
            # Insert sample tenants
            tenants_data = [
                ('Tech Solutions Inc.', 'contact@techsolutions.com', '+1234567890', 
                 '123 Tech Street, Silicon Valley', 'premium'),
                ('Global Retail Corp.', 'info@globalretail.com', '+0987654321', 
                 '456 Retail Ave, Business District', 'basic'),
                ('Local Services LLC', 'support@localservices.com', '+1122334455', 
                 '789 Service Blvd, Downtown', 'standard')
            ]
            
            tenant_ids = []
            for tenant_data in tenants_data:
                cursor.execute("""
                    INSERT INTO tenants (business_name, contact_email, contact_phone, address, subscription_plan)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING tenant_id
                """, tenant_data)
                
                tenant_id = cursor.fetchone()[0]
                tenant_ids.append(tenant_id)
                self.stdout.write(f"Created tenant: {tenant_data[0]} (ID: {tenant_id})")
            
            # Insert sample users
            users_data = [
                (tenant_ids[0], 'John Admin', 'john.admin@techsolutions.com', 'hashed_password_1', 'admin'),
                (tenant_ids[0], 'Jane Manager', 'jane.manager@techsolutions.com', 'hashed_password_2', 'manager'),
                (tenant_ids[0], 'Jim User', 'jim.user@techsolutions.com', 'hashed_password_3', 'user'),
                (tenant_ids[1], 'Alice Admin', 'alice.admin@globalretail.com', 'hashed_password_4', 'admin'),
                (tenant_ids[1], 'Bob User', 'bob.user@globalretail.com', 'hashed_password_5', 'user'),
                (tenant_ids[2], 'Carol Admin', 'carol.admin@localservices.com', 'hashed_password_6', 'admin')
            ]
            
            user_ids = []
            for user_data in users_data:
                cursor.execute("""
                    INSERT INTO users (tenant_id, name, email, password_hash, role)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING user_id
                """, user_data)
                
                user_id = cursor.fetchone()[0]
                user_ids.append(user_id)
                self.stdout.write(f"Created user: {user_data[1]} (ID: {user_id})")
            
            # Insert sample products
            products_data = [
                # Tech Solutions Inc. products
                (tenant_ids[0], 'Laptop Model X', 'LAPTOP-X-001', 50, 800.00, 1200.00),
                (tenant_ids[0], 'Wireless Mouse Pro', 'MOUSE-P-002', 200, 15.00, 35.00),
                (tenant_ids[0], 'USB-C Hub', 'HUB-C-003', 75, 25.00, 45.00),
                
                # Global Retail Corp. products
                (tenant_ids[1], 'Office Chair Deluxe', 'CHAIR-D-001', 30, 75.00, 150.00),
                (tenant_ids[1], 'Desk Lamp LED', 'LAMP-L-002', 100, 20.00, 45.00),
                (tenant_ids[1], 'Filing Cabinet', 'CABINET-003', 25, 80.00, 140.00),
                
                # Local Services LLC products
                (tenant_ids[2], 'Toolbox Set', 'TOOLBOX-001', 40, 45.00, 85.00),
                (tenant_ids[2], 'Power Drill', 'DRILL-002', 15, 60.00, 110.00),
                (tenant_ids[2], 'Measuring Tape', 'TAPE-003', 150, 5.00, 12.00)
            ]
            
            product_ids = []
            for product_data in products_data:
                cursor.execute("""
                    INSERT INTO products (tenant_id, product_name, sku, quantity, buying_price, selling_price)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING product_id
                """, product_data)
                
                product_id = cursor.fetchone()[0]
                product_ids.append(product_id)
                self.stdout.write(f"Created product: {product_data[2]} (ID: {product_id})")
            
            # Commit changes
            conn.commit()
            
            # Display summary
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully initialized IMS database with:\n'
                    f'- {len(tenant_ids)} tenants\n'
                    f'- {len(user_ids)} users\n'
                    f'- {len(product_ids)} products'
                )
            )
            
            # Close connection
            cursor.close()
            conn.close()
            
        except psycopg2.Error as e:
            self.stdout.write(
                self.style.ERROR(f'Database error: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {e}')
            )