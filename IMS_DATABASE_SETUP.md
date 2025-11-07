# Multi-Tenant Inventory Management System (IMS) Database Setup

This document provides instructions for setting up the PostgreSQL database for the Multi-Tenant Inventory Management System.

## Database Structure

The IMS database consists of three main tables:

1. **tenants**: Stores business details for each company using the IMS
2. **users**: Stores user accounts linked to tenants
3. **products**: Stores product details linked to tenants

## Prerequisites

- PostgreSQL server installed and running
- Python 3.8+ with psycopg2 package installed
- This project's dependencies installed (`pip install -r requirements.txt`)

## Setup Instructions

### 1. Create Database and Tables

Run the database setup script:

```bash
setup_ims_db.bat
```

This script will:
- Create the `ims_db` database
- Create the `ims_user` database user
- Create all required tables with proper relationships
- Test the database connection

### 2. Manual Database Creation (Alternative)

If you prefer to create the database manually:

1. Connect to PostgreSQL as a superuser:
   ```bash
   psql -U postgres
   ```

2. Run the SQL script:
   ```bash
   psql -U postgres -f create_ims_db.sql
   ```

### 3. Test Database Connection

Run the Python test script to verify the connection:

```bash
python test_ims_db_connection.py
```

## Database Schema

### Tenants Table

| Column | Type | Description |
|--------|------|-------------|
| tenant_id | SERIAL (Primary Key) | Unique identifier for each tenant |
| business_name | VARCHAR(255) | Name of the business |
| contact_email | VARCHAR(255) UNIQUE | Contact email (unique) |
| contact_phone | VARCHAR(20) | Contact phone number |
| address | TEXT | Business address |
| subscription_plan | VARCHAR(50) | Subscription plan (default: 'basic') |
| status | VARCHAR(20) | Status with CHECK constraint (active, inactive, suspended) |
| created_at | TIMESTAMP | Creation timestamp (default: CURRENT_TIMESTAMP) |
| updated_at | TIMESTAMP | Last update timestamp (default: CURRENT_TIMESTAMP) |

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| user_id | SERIAL (Primary Key) | Unique identifier for each user |
| tenant_id | INTEGER (Foreign Key) | References tenants.tenant_id |
| name | VARCHAR(255) | User's full name |
| email | VARCHAR(255) UNIQUE | User's email (unique) |
| password_hash | VARCHAR(255) | Hashed password |
| role | VARCHAR(50) | Role with CHECK constraint (admin, manager, user) |
| created_at | TIMESTAMP | Creation timestamp (default: CURRENT_TIMESTAMP) |
| updated_at | TIMESTAMP | Last update timestamp (default: CURRENT_TIMESTAMP) |

### Products Table

| Column | Type | Description |
|--------|------|-------------|
| product_id | SERIAL (Primary Key) | Unique identifier for each product |
| tenant_id | INTEGER (Foreign Key) | References tenants.tenant_id |
| product_name | VARCHAR(255) | Name of the product |
| sku | VARCHAR(100) UNIQUE | Stock Keeping Unit (unique) |
| quantity | INTEGER | Quantity with CHECK constraint (>= 0) |
| buying_price | DECIMAL(10, 2) | Price the product was bought for |
| selling_price | DECIMAL(10, 2) | Price the product is sold for |
| created_at | TIMESTAMP | Creation timestamp (default: CURRENT_TIMESTAMP) |
| updated_at | TIMESTAMP | Last update timestamp (default: CURRENT_TIMESTAMP) |

## Data Integrity & Constraints

1. **Primary Keys**: All tables use SERIAL or BIGSERIAL for primary keys
2. **Foreign Keys**: Proper relationships between tables using tenant_id
3. **Uniqueness**: Emails and SKUs are unique across the system
4. **Check Constraints**: 
   - Product quantity must be >= 0
   - Tenant status must be one of: 'active', 'inactive', 'suspended'
   - User role must be one of: 'admin', 'manager', 'user'
5. **Timestamps**: All tables have created_at and updated_at columns with default CURRENT_TIMESTAMP

## Tenant Isolation

The multi-tenant architecture ensures data isolation between different businesses:

- Each tenant can only access their own data
- All queries must be filtered by tenant_id
- Foreign key constraints ensure data consistency

## Connection Configuration

To use the new database with Django, update your settings to use the new configuration file:

1. Rename `inventory_management/ims_local_settings.py` to `inventory_management/local_settings.py`
2. Or modify the existing `local_settings.py` to use the new database credentials

## Backup and Recovery

### Schema Backup

To backup the database schema:

```bash
backup_ims_schema.bat
```

This creates a backup of the database structure without data in the `backups/` directory.

### Full Database Backup

To backup the entire database (schema + data):

```bash
pg_dump -U ims_user -h localhost -p 5432 ims_db > backups/ims_full_backup.sql
```

## Testing

The connection test script performs the following validations:

1. Basic database connection
2. Table existence verification
3. Sample data insertion and retrieval
4. Tenant isolation verification

## Troubleshooting

### Connection Issues

1. Ensure PostgreSQL is running
2. Verify database credentials in the connection scripts
3. Check that the `ims_user` has proper privileges

### Permission Issues

1. Ensure the `ims_user` has been granted all necessary privileges
2. Check that the user can connect to the database

### Data Integrity Issues

1. Verify that all CHECK constraints are properly defined
2. Ensure foreign key relationships are correctly established

## Next Steps

1. Configure Django to use the new database
2. Run Django migrations to create any additional tables needed
3. Create superuser accounts for administration
4. Implement tenant context middleware for automatic tenant_id filtering