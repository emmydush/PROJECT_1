# PowerShell script to automatically set up the PostgreSQL IMS database

Write-Host "Automatic Setup of PostgreSQL IMS Database"
Write-Host "========================================="

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion"
} catch {
    Write-Host "Error: Python not found. Please ensure Python is installed and added to PATH."
    pause
    exit 1
}

# Check if psycopg2 is available
try {
    python -c "import psycopg2" 2>&1 > $null
    Write-Host "✓ psycopg2 found"
} catch {
    Write-Host "Installing psycopg2..."
    pip install psycopg2-binary
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install psycopg2. Please install it manually using 'pip install psycopg2-binary'"
        pause
        exit 1
    }
}

Write-Host "Starting automatic database setup..."
Write-Host ""

# Run the Python setup script
python auto_setup_ims_db.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error: Automatic database setup failed."
    pause
    exit 1
}

Write-Host ""
Write-Host "Database setup completed successfully!"
Write-Host ""

pause