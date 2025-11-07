@echo off
REM Batch script to set up the PostgreSQL IMS database

echo Setting up PostgreSQL IMS database...
echo ======================================

REM Check if psql is available
where psql >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: psql not found. Please ensure PostgreSQL is installed and added to PATH.
    pause
    exit /b 1
)

echo Creating IMS database and user...
echo --------------------------------

REM Run the SQL script to create database and tables
psql -U postgres -f create_ims_db.sql

if %errorlevel% neq 0 (
    echo Error: Failed to create database.
    pause
    exit /b 1
)

echo.
echo Database setup completed successfully!
echo.

echo Testing database connection...
echo ------------------------------

REM Run the Python connection test
python test_ims_db_connection.py

if %errorlevel% neq 0 (
    echo Error: Database connection test failed.
    pause
    exit /b 1
)

echo.
echo All steps completed successfully!
echo The IMS database is ready for use.
echo.

pause