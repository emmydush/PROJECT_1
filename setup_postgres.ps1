# PowerShell script to set up PostgreSQL database and user for Inventory Management System

# Add PostgreSQL to PATH
$env:PATH += ";C:\Program Files\PostgreSQL\17\bin"

# Database configuration
$DB_NAME = "inventory_management"
$DB_USER = "inventory_user"
$DB_PASSWORD = "inventory_password"

# Drop existing database and user if they exist
echo "Dropping existing database and user (if they exist)..."
psql -U postgres -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>$null
psql -U postgres -c "DROP USER IF EXISTS $DB_USER;" 2>$null

# Create new database and user
echo "Creating PostgreSQL database and user..."

# Create user with password
psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
if ($LASTEXITCODE -eq 0) {
    echo "User $DB_USER created successfully"
} else {
    echo "Error creating user $DB_USER"
}

# Create database
psql -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
if ($LASTEXITCODE -eq 0) {
    echo "Database $DB_NAME created successfully"
} else {
    echo "Error creating database $DB_NAME"
}

# Grant privileges
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
echo "Granted privileges to user $DB_USER on database $DB_NAME"

echo "PostgreSQL setup completed!"
echo "You can now run Django migrations to create the tables."