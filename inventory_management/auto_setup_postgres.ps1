# PowerShell script to automatically set up PostgreSQL database and user
# This script uses the psql command-line tool to create the database and user

Write-Host "Automatic PostgreSQL Setup for Inventory Management System" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""

# Check if PostgreSQL bin directory exists
$psqlPath = "C:\Program Files\PostgreSQL\17\bin\psql.exe"
if (-not (Test-Path $psqlPath)) {
    # Try alternative PostgreSQL versions
    $pgPath = "C:\Program Files\PostgreSQL"
    if (Test-Path $pgPath) {
        $versions = Get-ChildItem $pgPath -Directory | Sort-Object Name -Descending
        foreach ($version in $versions) {
            $possiblePath = Join-Path $pgPath $version.Name "bin\psql.exe"
            if (Test-Path $possiblePath) {
                $psqlPath = $possiblePath
                break
            }
        }
    }
}

if (-not (Test-Path $psqlPath)) {
    Write-Host "Error: Could not find psql.exe. Please ensure PostgreSQL is installed." -ForegroundColor Red
    Write-Host "Expected location: C:\Program Files\PostgreSQL\[version]\bin\psql.exe" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found psql at: $psqlPath" -ForegroundColor Yellow
Write-Host ""

# Database configuration
$databaseName = "inventory_management"
$username = "inventory_user"
$password = "Jesuslove@12"

Write-Host "Creating database and user with the following configuration:" -ForegroundColor Cyan
Write-Host "  Database: $databaseName" -ForegroundColor White
Write-Host "  Username: $username" -ForegroundColor White
Write-Host "  Password: $password" -ForegroundColor White
Write-Host "  Host: localhost" -ForegroundColor White
Write-Host "  Port: 5432" -ForegroundColor White
Write-Host ""

# Set environment variable for password
$env:PGPASSWORD = "Jesuslove@12"

try {
    Write-Host "Step 1: Creating user..." -ForegroundColor Yellow
    # Create user command
    & $psqlPath -U postgres -h localhost -p 5432 -c "CREATE USER $username WITH PASSWORD '$password';" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: User created successfully!" -ForegroundColor Green
    } else {
        Write-Host "INFO: User may already exist, continuing..." -ForegroundColor Yellow
    }
    
    Write-Host "Step 2: Creating database..." -ForegroundColor Yellow
    # Create database command
    & $psqlPath -U postgres -h localhost -p 5432 -c "CREATE DATABASE $databaseName OWNER $username;" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Database created successfully!" -ForegroundColor Green
    } else {
        Write-Host "INFO: Database may already exist, continuing..." -ForegroundColor Yellow
    }
    
    Write-Host "Step 3: Granting privileges..." -ForegroundColor Yellow
    # Grant privileges
    & $psqlPath -U postgres -h localhost -p 5432 -c "GRANT ALL PRIVILEGES ON DATABASE $databaseName TO $username;" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Privileges granted successfully!" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "SUCCESS: PostgreSQL setup completed successfully!" -ForegroundColor Green
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
} catch {
    Write-Host "Error occurred during setup: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "You may need to manually create the database and user using pgAdmin." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Instructions:" -ForegroundColor Cyan
    Write-Host "1. Open pgAdmin" -ForegroundColor White
    Write-Host "2. Create a new database named 'inventory_management'" -ForegroundColor White
    Write-Host "3. Create a new user named 'inventory_user' with password 'Jesuslove@12'" -ForegroundColor White
    Write-Host "4. Grant all privileges on the database to the user" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..."
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")