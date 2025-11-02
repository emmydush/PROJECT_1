# PostgreSQL Setup Guide

This document explains how to configure the Inventory Management System to use PostgreSQL instead of SQLite.

## Prerequisites

1. PostgreSQL server installed and running
2. A PostgreSQL database created for the application
3. A PostgreSQL user with appropriate permissions
4. pgAdmin for database management

## Setup Instructions

1. **Update local_settings.py**
   The local_settings.py file in the `inventory_management` directory has already been configured with your PostgreSQL credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'inventory_management',
           'USER': 'inventory_user',
           'PASSWORD': 'Jesuslove@12',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

2. **Automatic Database Setup (Recommended)**
   We've provided automatic setup scripts that will create the database and user for you:
   
   ### Using Windows Batch Script (Easiest)
   Double-click on `auto_setup_postgres.bat` or run from command line:
   ```cmd
   auto_setup_postgres.bat
   ```
   
   ### Using PowerShell Script Directly
   ```powershell
   .\auto_setup_postgres.ps1
   ```

3. **Manual Database Setup Using pgAdmin**
   If the automatic setup doesn't work, you can create the database and user manually using pgAdmin:
   
   ### Using pgAdmin
   1. Open pgAdmin
   2. If prompted, enter your pgAdmin password: `Jesuslove@12`
   3. In the left sidebar, expand the server connection
   4. Right-click on "Databases" and select "Create" > "Database..."
   5. In the "Create - Database" dialog:
      - Name: `inventory_management`
      - Leave other settings as default
      - Click "Save"
   
   6. Create a new user:
      - Right-click on "Login/Group Roles" and select "Create" > "Login/Group Role..."
      - In the "General" tab:
        - Name: `inventory_user`
      - In the "Definition" tab:
        - Password: `Jesuslove@12`
        - Confirm Password: `Jesuslove@12`
        - Uncheck "Can log in?" and then check it again (to ensure it's enabled)
      - In the "Privileges" tab:
        - Toggle "Superuser" to "Yes" (for development purposes)
        - Toggle "Can login?" to "Yes"
      - Click "Save"
   
   7. Grant privileges to the user:
      - Right-click on the "inventory_management" database and select "Properties"
      - Go to the "Security" tab
      - Click the "+" button to add a new privilege
      - In the "Grantee" dropdown, select "inventory_user"
      - Check all privileges in the "Privileges" column
      - Click "Save"

4. **Alternative: Create Database and User Using SQL Commands**
   If you prefer to use SQL commands directly:
   
   ```sql
   -- Connect to PostgreSQL as a superuser first
   -- Then run these commands:
   
   -- Create the database
   CREATE DATABASE inventory_management;
   
   -- Create a dedicated user for the application
   CREATE USER inventory_user WITH PASSWORD 'Jesuslove@12';
   
   -- Grant privileges to the user on the database
   GRANT ALL PRIVILEGES ON DATABASE inventory_management TO inventory_user;
   
   -- Connect to the newly created database
   \c inventory_management
   
   -- Grant schema privileges
   GRANT ALL ON SCHEMA public TO inventory_user;
   ```

5. **Install Required Dependencies**
   Make sure you have the required packages installed:
   ```bash
   pip install -r requirements.txt
   ```
   The `psycopg2-binary` package should already be included in requirements.txt.

6. **Run Migrations**
   After configuring PostgreSQL and creating the database/user, run the migrations to create the database schema:
   ```bash
   # From the project root directory (where manage.py is located)
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a Superuser (Optional)**
   ```bash
   # From the project root directory (where manage.py is located)
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user:
   - Username: (enter your preferred admin username)
   - Email address: (enter your email)
   - Password: (enter a secure password)
   - Password (again): (confirm your password)

8. **Test the Configuration**
   Run the development server to verify everything is working:
   ```bash
   # From the project root directory (where manage.py is located)
   python manage.py runserver
   ```

## Completely Removing SQLite

To completely remove SQLite and ensure the application only uses PostgreSQL:

1. **Modified Settings**: The settings.py file has been updated to remove the SQLite fallback and now requires PostgreSQL configuration.

2. **Delete SQLite Database File**: 
   - If the db.sqlite3 file is not in use, you can delete it directly
   - If it's in use, restart your computer and delete it then
   - Alternatively, run the DELETE_SQLITE_DB.bat script provided in the project root

3. **Verify Configuration**: 
   Run the test script to verify the application is using PostgreSQL:
   ```bash
   python inventory_management/test_db_connection.py
   ```

## Troubleshooting

- **Connection Refused**: Ensure PostgreSQL is running and accepting connections on the specified host and port.
- **Authentication Failed**: Verify the username and password in your local_settings.py file.
- **Database Does Not Exist**: Make sure you've created the database in PostgreSQL.
- **Permission Denied**: Ensure your PostgreSQL user has the necessary permissions.
- **Script Execution Policy Error**: If you get an error about execution policy when running the PowerShell script, run this command in PowerShell as Administrator:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
  ```

## Reverting to SQLite

If you need to revert to SQLite, you would need to:
1. Restore the original settings.py database configuration
2. Create a new local_settings.py file without the DATABASES configuration