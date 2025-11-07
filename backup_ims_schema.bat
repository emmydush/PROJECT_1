@echo off
REM Batch script to backup the PostgreSQL IMS database schema

echo Backing up PostgreSQL IMS database schema...
echo ===========================================

REM Check if pg_dump is available
where pg_dump >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pg_dump not found. Please ensure PostgreSQL is installed and added to PATH.
    pause
    exit /b 1
)

REM Create backups directory if it doesn't exist
if not exist "backups" mkdir "backups"

REM Get current date for backup filename
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"
set "datestamp=%YY%-%MM%-%DD%"

REM Backup database schema only (no data)
pg_dump -U postgres -h localhost -p 5432 --schema-only --no-owner --no-privileges ims_db > backups/ims_schema_%datestamp%.sql

if %errorlevel% neq 0 (
    echo Error: Failed to backup database schema.
    pause
    exit /b 1
)

echo.
echo Database schema backed up successfully to backups/ims_schema_%datestamp%.sql
echo.

pause