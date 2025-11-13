# Local Settings Override for Development
# This file forces the use of local database settings

# Database Configuration for IMS
# Using PostgreSQL for production environment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ims_db',
        'USER': 'postgres',
        'PASSWORD': 'Jesuslove@12',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Force DEBUG mode for development
DEBUG = True

# Allow all hosts for development
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Secret key for development
SECRET_KEY = 'django-insecure-j@z%a^!@+m07654321zyxwvutsrqponmlkjihgfedcba'

# Custom user model
AUTH_USER_MODEL = 'authentication.User'

# Static files configuration
STATIC_URL = '/static/'
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type (fixes migration warnings)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Installed apps from main settings
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'dashboard',
    'products',
    'sales',
    'purchases',
    'expenses',
    'customers',
    'suppliers',
    'reports',
    'settings',
    'notifications',
    'superadmin',
    'api',
]