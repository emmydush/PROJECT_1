# Render Deployment Guide

This project is now fully configured for deployment on Render. Follow these steps to deploy:

## Prerequisites
- A Render account (free tier available at https://render.com)
- GitHub account with this repository connected
- PostgreSQL database (Render offers free tier)

## Step 1: Prepare Environment Variables

Copy the values from `.env.example` and prepare the following for Render:

```env
DEBUG=False
SECRET_KEY=<generate-a-random-secure-string>
ALLOWED_HOSTS=<your-render-domain>.onrender.com,www.<your-render-domain>.onrender.com
DATABASE_URL=<your-postgresql-connection-string>
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=<your-email@gmail.com>
EMAIL_HOST_PASSWORD=<your-app-password>
EMAIL_USE_TLS=True
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Generate a Secure SECRET_KEY

Run this Python command locally:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Step 2: Create Render Services

### 2.1 PostgreSQL Database
1. Go to Render Dashboard → New +
2. Select PostgreSQL
3. Configure:
   - Name: `inventory-db`
   - Database: `inventory_db`
   - User: `postgres`
   - Region: Choose your closest region
4. Copy the connection string (shown after creation)

### 2.2 Web Service
1. Go to Render Dashboard → New +
2. Select Web Service
3. Connect your GitHub repository
4. Configure:
   - Name: `smart-solution-api`
   - Environment: Docker
   - Region: Same as database
   - Scaling Plan: Free tier recommended for testing
5. Set environment variables (Add from `.env.example`)
6. Deploy

## Step 3: Configure Render Environment

In the Render dashboard for your Web Service:

1. Go to Environment tab
2. Add all variables from `.env.example`:
   - `DEBUG=False`
   - `SECRET_KEY=<your-generated-key>`
   - `ALLOWED_HOSTS=<render-domain>`
   - `DATABASE_URL=<from-postgres-service>`
   - Email settings
   - Security settings

3. Deploy changes

## Step 4: Monitor Deployment

1. Go to Logs tab to see deployment progress
2. Check for any errors during:
   - Docker build
   - Migrations
   - Static file collection
   - Gunicorn startup

## Troubleshooting

### Issue: "ProgrammingError: relation does not exist"
**Solution:** Migrations are running but database tables weren't created. Check Render logs for:
```
python manage.py migrate
```

The `Procfile` release command should handle this automatically.

### Issue: Static files not loading
**Solution:** Run manually in Render terminal:
```bash
python manage.py collectstatic --noinput
```

Or check that `STATIC_URL` and `STATIC_ROOT` are correctly set in `settings.py`.

### Issue: Database connection refused
**Solution:** Verify:
1. `DATABASE_URL` environment variable is set correctly
2. PostgreSQL service is running on Render
3. Check database connection string format: `postgresql://user:password@host:port/dbname`

### Issue: Gunicorn worker timeout
**Solution:** Increase worker count in `docker-entrypoint.sh`:
```bash
exec gunicorn inventory_management.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 8 \  # Increase if needed
  --worker-class sync \
  --timeout 120  # Increase timeout if needed
```

## Production Checklist

- [ ] `DEBUG=False` in Render environment
- [ ] `SECRET_KEY` is a secure random string
- [ ] `ALLOWED_HOSTS` includes your Render domain
- [ ] `DATABASE_URL` points to PostgreSQL database
- [ ] Email settings configured (Gmail or SendGrid recommended)
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] First migration runs successfully
- [ ] Static files collect without errors
- [ ] Login page loads at https://your-domain/accounts/login/
- [ ] Dashboard accessible after login

## Post-Deployment

1. **Create Superuser:**
   ```bash
   # Use Render shell:
   python manage.py createsuperuser
   ```

2. **Access Admin Panel:**
   ```
   https://your-domain/admin/
   ```

3. **Set Up Monitoring:**
   - Use Render's logs and alerts
   - Configure email notifications for deployment failures

4. **Backup Database:**
   - Use Render's PostgreSQL backup feature
   - Configure automated daily backups

## Security Notes

- Never commit `.env` file or actual secrets
- Use `.env.example` as a template only
- Rotate `SECRET_KEY` periodically
- Keep dependencies updated: `pip list --outdated`
- Monitor Render security advisories

## Useful Render Commands

Access Render Shell:
```bash
# In Render Dashboard → Web Service → Shell

# View logs
tail -f /var/log/gunicorn.log

# Run management commands
python manage.py shell
python manage.py createsuperuser
python manage.py collectstatic --noinput

# Check disk space
df -h
```

## Need Help?

- Render Documentation: https://docs.render.com
- Django Deployment: https://docs.djangoproject.com/en/5.1/howto/deployment/
- This project's README: See README.md

---

**Last Updated:** November 2025
**Django Version:** 5.1.7
**Python Version:** 3.12.0
