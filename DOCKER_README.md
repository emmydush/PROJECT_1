# Docker Setup for Inventory Management System

This document explains how to containerize the Inventory Management System using Docker and Docker Compose.

## Prerequisites

1. Docker Desktop (for Windows/Mac) or Docker Engine (for Linux)
2. Docker Compose

## Files Created

1. `Dockerfile` - Defines the Django application container
2. `docker-compose.yml` - Defines and orchestrates both the Django app and PostgreSQL database containers
3. `.dockerignore` - Specifies files and directories to exclude from the Docker build
4. `wait-for-db.py` - Script to wait for the database to be ready before starting the Django app
5. `docker-entrypoint.sh` - Entrypoint script for the Django container

## Docker Configuration Details

### Dockerfile
- Uses Python 3.12 slim image as base
- Installs system dependencies including PostgreSQL client
- Copies requirements and installs Python packages
- Sets up a non-root user for security
- Exposes port 8000 for the Django application

### docker-compose.yml
- Defines two services: `web` (Django app) and `db` (PostgreSQL)
- Uses PostgreSQL 15 image
- Configures database credentials to match local_settings.py
- Sets up volumes for persistent data storage
- Includes health checks for the database
- Maps ports for external access

### Environment Configuration
The application automatically detects when running in Docker through the `DATABASE_URL` environment variable and configures the database connection accordingly.

## How to Use

1. Make sure Docker Desktop is running
2. Open a terminal in the project root directory
3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```
4. The application will be available at http://localhost:8000
5. The PostgreSQL database will be available at localhost:5432

## Useful Docker Commands

- View logs: `docker-compose logs -f`
- Stop containers: `docker-compose down`
- Rebuild containers: `docker-compose up -d --build`
- Access Django container shell: `docker-compose exec web bash`
- Access PostgreSQL container shell: `docker-compose exec db bash`

## First-time Setup

On first run, the application will:
1. Wait for the database to be ready
2. Run migrations to set up the database schema
3. Collect static files
4. Create test users (admin, manager, cashier, stockmanager)

## Default Test Users

After the first run, you can log in with these credentials:

1. Admin User:
   - Username: admin
   - Password: admin123

2. Manager User:
   - Username: manager
   - Password: manager123

3. Cashier User:
   - Username: cashier
   - Password: cashier123

4. Stock Manager User:
   - Username: stockmanager
   - Password: stockmanager123

## Data Persistence

The PostgreSQL data is stored in a Docker volume named `postgres_data`, which persists even when containers are deleted. To completely reset the database, you would need to remove this volume:

```bash
docker-compose down -v
```

## Troubleshooting

If you encounter issues:

1. Make sure Docker Desktop is running
2. Check that ports 8000 and 5432 are not being used by other applications
3. View logs with `docker-compose logs -f` to see any error messages
4. Ensure you have sufficient disk space and memory allocated to Docker

## Customization

You can modify the following in `docker-compose.yml`:
- Database credentials (be sure to update local_settings.py accordingly)
- Port mappings
- Volume mappings for static and media files
- Environment variables