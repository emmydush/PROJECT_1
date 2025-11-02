# PowerShell script to set up PostgreSQL database and user for Inventory Management System

Write-Host "Setting up PostgreSQL database and user for Inventory Management System..." -ForegroundColor Green
Write-Host ""

# Check if psql is available
try {
    $psqlPath = Get-Command psql -ErrorAction Stop
    Write-Host "Found psql at: $($psqlPath.Source)" -ForegroundColor Yellow
} catch {
    Write-Host "Error: psql not found. Please ensure PostgreSQL is installed and added to PATH." -ForegroundColor Red
    Write-Host "You may need to run this script from the PostgreSQL bin directory or add it to your PATH." -ForegroundColor Red
    Pause
    exit 1
}

# Run the SQL script to create database and user
Write-Host "Creating database and user..." -ForegroundColor Yellow
try {
    psql -U postgres -f create_postgres_db.sql
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Database and user created successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Run migrations to create tables:" -ForegroundColor Cyan
        Write-Host "   python manage.py makemigrations" -ForegroundColor White
        Write-Host "   python manage.py migrate" -ForegroundColor White
        Write-Host ""
        Write-Host "2. Create a superuser:" -ForegroundColor Cyan
        Write-Host "   python manage.py createsuperuser" -ForegroundColor White
        Write-Host ""
        Write-Host "3. Start the development server:" -ForegroundColor Cyan
        Write-Host "   python manage.py runserver" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "Error occurred while creating database and user." -ForegroundColor Red
        Write-Host "Please check the error message above." -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "Error occurred while creating database and user: $_" -ForegroundColor Red
}

Pause