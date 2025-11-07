@echo off
REM Batch script to automatically set up the PostgreSQL IMS database

echo Automatic Setup of PostgreSQL IMS Database
echo =========================================

REM Check if Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please ensure Python is installed and added to PATH.
    pause
    exit /b 1
)

REM Check if psycopg2 is available
python -c "import psycopg2" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: psycopg2 not found. Installing psycopg2...
    pip install psycopg2-binary
    if %errorlevel% neq 0 (
        echo Error: Failed to install psycopg2. Please install it manually using 'pip install psycopg2-binary'
        pause
        exit /b 1
    )
)

echo Starting automatic database setup...
echo.

REM Run the Python setup script
python auto_setup_ims_db.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Automatic database setup failed.
    pause
    exit /b 1
)

echo.
echo Database setup completed successfully!
echo.

pause