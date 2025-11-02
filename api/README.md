# Inventory Management System API

## Overview
This is a REST API for the Inventory Management System, designed to provide a scalable backend that can support web, mobile, and POS applications.

## Features
- RESTful API design
- Token-based authentication
- Filtering and search capabilities
- Pagination
- CORS support
- Comprehensive documentation

## Technology Stack
- Django REST Framework
- Django CORS Headers
- Django Filter

## API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/register/` - User registration
- `GET /api/v1/auth/profile/` - Get user profile

### Products
- `GET /api/v1/products/` - List all products
- `POST /api/v1/products/create/` - Create a new product
- `GET /api/v1/products/{id}/` - Get product details
- `PUT /api/v1/products/{id}/update/` - Update a product
- `DELETE /api/v1/products/{id}/delete/` - Delete a product

### Sales
- `GET /api/v1/sales/` - List all sales
- `POST /api/v1/sales/create/` - Create a new sale
- `GET /api/v1/sales/{id}/` - Get sale details

### Dashboard
- `GET /api/v1/dashboard/stats/` - Get dashboard statistics

## Installation
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Add the following to your Django settings:
   ```python
   INSTALLED_APPS = [
       # ... other apps
       'api',
       'rest_framework',
       'corsheaders',
       'django_filters',
   ]

   MIDDLEWARE = [
       # ... other middleware
       'corsheaders.middleware.CorsMiddleware',
   ]

   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.SessionAuthentication',
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
       'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
       'PAGE_SIZE': 20,
   }
   ```

3. Include the API URLs in your main urls.py:
   ```python
   urlpatterns = [
       # ... other patterns
       path('api/v1/', include('api.urls')),
   ]
   ```

## Usage
1. Start the development server:
   ```
   python manage.py runserver
   ```

2. Access the API documentation at:
   ```
   http://localhost:8000/api/v1/
   ```

## Authentication
Most endpoints require authentication. You can authenticate using:
1. Session authentication (login through the web interface)
2. Token authentication (obtained through login endpoint)

## Filtering and Search
The API supports filtering and search on most list endpoints:
- Filter by field: `/api/v1/products/?category=1`
- Search: `/api/v1/products/?search=laptop`
- Ordering: `/api/v1/products/?ordering=name`

## Pagination
List endpoints are paginated by default with 20 items per page.

## CORS
CORS is configured to allow requests from common development origins.

## Testing
Run tests with:
```
python manage.py test api
```