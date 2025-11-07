@echo off
cd /d E:\AI
call venv_new\Scripts\activate.bat

echo ====================================================
echo MULTI-TENANT INVENTORY MANAGEMENT SYSTEM
echo EMERGENCY ROLLBACK PROCEDURE
echo ====================================================
echo.
echo This script will:
echo 1. List available backups
echo 2. Restore from selected backup
echo 3. Rollback migrations if needed
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo Starting rollback process...
echo.

python rollback_migration.py

echo.
echo Rollback process completed.
echo Check rollback_log.txt for detailed logs.
echo.
pause