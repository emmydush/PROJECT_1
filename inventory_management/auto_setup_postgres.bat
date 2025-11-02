@echo off
REM Batch file to run the PowerShell script for automatic PostgreSQL setup

echo Automatic PostgreSQL Setup for Inventory Management System
echo ========================================================
echo.

REM Check if PowerShell is available
where powershell >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: PowerShell not found.
    echo Please ensure PowerShell is installed and available in your PATH.
    pause
    exit /b 1
)

echo Running PowerShell script to set up PostgreSQL...
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0auto_setup_postgres.ps1"

if %errorlevel% neq 0 (
    echo.
    echo Error occurred while running the PowerShell script.
    echo Please check the error message above.
)

pause