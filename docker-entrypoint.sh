#!/bin/bash

# Wait for database to be ready
python wait-for-db.py

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create test users if they don't exist
echo "Creating test users..."
python manage.py create_test_users

# Start the server
echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000