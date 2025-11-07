# Multi-Tenant Inventory Management System (IMS) - PostgreSQL Setup

This directory contains all the necessary files to set up and manage the PostgreSQL database for the Multi-Tenant Inventory Management System.

## Files Overview

### Database Setup Files
- [create_ims_db.sql](create_ims_db.sql) - SQL script to create the database, user, and tables
- [setup_ims_db.bat](setup_ims_db.bat) - Automated Windows batch script to set up the database
- [test_ims_db_connection.py](test_ims_db_connection.py) - Python script to test database connection and functionality
- [auto_setup_ims_db.py](auto_setup_ims_db.py) - Fully automated Python script to create database and tables
- [auto_setup_ims_db.bat](auto_setup_ims_db.bat) - Windows batch script to run automatic setup
- [auto_setup_ims_db.ps1](auto_setup_ims_db.ps1) - PowerShell script to run automatic setup

### Configuration Files
- [inventory_management/ims_local_settings.py](inventory_management/ims_local_settings.py) - Django settings for the new database
- [IMS_DATABASE_SETUP.md](IMS_DATABASE_SETUP.md) - Detailed documentation for database setup

### Migration Files
- [ims_migrations/0001_initial_schema.sql](ims_migrations/0001_initial_schema.sql) - Initial database schema
- [ims_migrations/0002_add_tenant_domains.sql](ims_migrations/0002_add_tenant_domains.sql) - Migration to add domain support
- [apply_ims_migrations.bat](apply_ims_migrations.bat) - Script to apply migrations

### Backup Files
- [backup_ims_schema.bat](backup_ims_schema.bat) - Script to backup database schema

## Quick Start

### Option 1: Fully Automatic Setup (Recommended)
1. Run the automatic setup script:
   ```
   auto_setup_ims_db.bat
   ```
   or
   ```
   .\auto_setup_ims_db.ps1
   ```

### Option 2: Manual Setup
1. Run the database setup:
   ```
   setup_ims_db.bat
   ```

2. Test the connection:
   ```
   python test_ims_db_connection.py
   ```

3. Apply migrations (if needed):
   ```
   apply_ims_migrations.bat
   ```

## Database Structure

The IMS database implements a multi-tenant architecture with three main tables:

1. **tenants** - Business entities using the system
2. **users** - User accounts associated with tenants
3. **products** - Product inventory associated with tenants

All tables are properly linked with foreign keys and include appropriate constraints for data integrity.

## Multi-Tenancy

The system ensures data isolation between tenants through:
- Foreign key relationships that enforce tenant context
- Queries that must always filter by tenant_id
- Proper indexing for performance

## Security

Database credentials:
- Database: `ims_db`
- User: `postgres`
- Password: `Jesuslove@12`

**Important**: Change these credentials in production environments.

## Backup and Recovery

Use the backup script to create schema backups:
```
backup_ims_schema.bat
```

For full database backups, use:
```
pg_dump -U postgres -h localhost -p 5432 ims_db > backup.sql
```

## Migration Management

To add new features or modify the schema:
1. Create a new migration file in the [ims_migrations](ims_migrations/) directory
2. Follow the naming convention: `NNNN_description.sql`
3. Apply migrations using [apply_ims_migrations.bat](apply_ims_migrations.bat)

## Troubleshooting

Common issues and solutions are documented in [IMS_DATABASE_SETUP.md](IMS_DATABASE_SETUP.md).

For connection issues:
1. Ensure PostgreSQL is running
2. Verify database credentials
3. Check that the `ims_user` has proper privileges