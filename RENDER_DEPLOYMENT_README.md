# Render Deployment Setup

This document outlines the steps for deploying the Inventory Management System to Render with a completely fresh start.

## Current State

The project has been prepared for a fresh Render deployment with:

1. **All migration files removed** - No existing migrations in any app
2. **Database completely cleaned** - All tables dropped
3. **Ready for fresh deployment** - Clean slate for Render

## Render Deployment Process

### 1. Environment Variables

Ensure the following environment variables are set in your Render service:

```
DATABASE_URL=your_render_postgresql_database_url
SECRET_KEY=your_production_secret_key
DEBUG=False
ALLOWED_HOSTS=your_render_domain.com,www.your_render_domain.com
```

### 2. Build Process

Render will automatically:
1. Install dependencies from `requirements.txt`
2. Run the application

### 3. Post-Deployment Setup

After deployment, run the setup script to initialize the database:

```bash
python render_setup.py
```

This script will:
- Create fresh migrations for all models
- Apply all migrations to set up the database schema
- Create a default superuser (admin/admin123)

### 4. Manual Steps (if needed)

If you need to run commands manually:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Verification

To verify the deployment is working:

1. Visit your Render domain
2. Check that the application loads without errors
3. Access the admin panel at `/admin/`
4. Log in with the default credentials (admin/admin123)

## Notes

- The database will be completely fresh with no existing data
- All models will be created from scratch
- Default superuser will be available for initial access
- You can change the default password after first login

This setup ensures a clean, fresh deployment suitable for production use on Render.