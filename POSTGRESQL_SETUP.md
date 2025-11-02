# PostgreSQL Setup for Inventory Management System

This document provides instructions for setting up PostgreSQL for the Inventory Management System.

## Prerequisites

- PostgreSQL server installed and running
- pgAdmin for database management
- This project's dependencies installed (`pip install -r requirements.txt`)

## Configuration Files

1. **Database Configuration**: The database settings are configured in `inventory_management/local_settings.py`
2. **Setup Guide**: Detailed instructions are available in `inventory_management/POSTGRESQL_SETUP.md`
3. **SQL Script**: Database creation script is available in `inventory_management/create_postgres_db.sql`

## Quick Start

1. Follow the instructions in `inventory_management/POSTGRESQL_SETUP.md` to create the database and user
2. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
4. Start the development server:
   ```
   python manage.py runserver
   ```

## Testing Database Connection

You can test the database connection using:
```
python inventory_management/test_db_connection.py
```

## Completely Removing SQLite

The application has been configured to use PostgreSQL exclusively. The SQLite fallback has been removed from the settings, and the application will no longer create or use a db.sqlite3 file.

If you still have a db.sqlite3 file:
1. Close all Python/Django processes
2. Delete the db.sqlite3 file in the project root directory
3. If the file is in use, restart your computer and delete it then

A script named DELETE_SQLITE_DB.bat has been provided to help with this process.

## Need Help?

If you encounter any issues during setup, refer to the detailed guide in `inventory_management/POSTGRESQL_SETUP.md` or check the troubleshooting section.