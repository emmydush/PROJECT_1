#!/bin/bash

# If DATABASE_URL is set (Render), extract host and port so other scripts
# that expect DB_HOST/DB_PORT (or wait-for-db.py) will work.
if [ -n "${DATABASE_URL:-}" ]; then
	# Use a small Python one-liner to parse the URL safely (no printing of secrets)
	export DB_HOST=$(python - <<'PY'
import os, urllib.parse
u = os.environ.get('DATABASE_URL', '')
if u:
		p = urllib.parse.urlparse(u)
		print(p.hostname or '')
else:
		print('')
PY
)
	export DB_PORT=$(python - <<'PY'
import os, urllib.parse
u = os.environ.get('DATABASE_URL', '')
if u:
		p = urllib.parse.urlparse(u)
		print(p.port or 5432)
else:
		print(5432)
PY
)
fi

# Wait for database to be ready
python wait-for-db.py

# Create new migrations based on model changes
echo "Creating migrations..."
python manage.py makemigrations

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create test users if they don't exist
echo "Creating test users..."
python manage.py create_test_users || true

# Start the server with Gunicorn for production
echo "Starting server with Gunicorn..."
exec gunicorn inventory_management.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4 --worker-class sync --timeout 60