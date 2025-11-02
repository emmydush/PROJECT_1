@echo off
REM Batch script to set up PostgreSQL database and user for Inventory Management System

echo Setting up PostgreSQL database and user for Inventory Management System...
echo.

REM Check if psql is available
where psql >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: psql not found. Please ensure PostgreSQL is installed and added to PATH.
    echo You may need to run this script from the PostgreSQL bin directory or add it to your PATH.
    pause
    exit /b 1
)

REM Run the SQL script to create database and user
echo Creating database and user...
psql -U postgres -f create_postgres_db.sql

if %errorlevel% equ 0 (
    echo.
    echo Database and user created successfully!
    echo.
    echo Next steps:
    echo 1. Run migrations to create tables:
    echo    python manage.py makemigrations
    echo    python manage.py migrate
    echo.
    echo 2. Create a superuser:
    echo    python manage.py createsuperuser
    echo.
    echo 3. Start the development server:
    echo    python manage.py runserver
) else (
    echo.
    echo Error occurred while creating database and user.
    echo Please check the error message above.
)

pause