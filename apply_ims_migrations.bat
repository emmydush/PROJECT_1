@echo off
REM Batch script to apply IMS database migrations

echo Applying IMS database migrations...
echo =================================

REM Check if psql is available
where psql >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: psql not found. Please ensure PostgreSQL is installed and added to PATH.
    pause
    exit /b 1
)

REM Apply initial schema migration
echo Applying initial schema migration...
psql -U postgres -d ims_db -h localhost -p 5432 -f ims_migrations/0001_initial_schema.sql

if %errorlevel% neq 0 (
    echo Error: Failed to apply initial schema migration.
    pause
    exit /b 1
)

REM Apply domain support migration
echo Applying domain support migration...
psql -U postgres -d ims_db -h localhost -p 5432 -f ims_migrations/0002_add_tenant_domains.sql

if %errorlevel% neq 0 (
    echo Error: Failed to apply domain support migration.
    pause
    exit /b 1
)

echo.
echo All migrations applied successfully!
echo.

pause