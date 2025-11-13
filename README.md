# Inventory Management System

A comprehensive inventory management system built with Django and PostgreSQL.

## Features

- Product Management
- Sales and Purchase Tracking
- Customer and Supplier Management
- Expense Tracking
- Reporting
- Multi-tenancy Support
- **Role-Based Access Control (RBAC)**

## Role-Based Access Control (RBAC)

This system implements a comprehensive Role-Based Access Control (RBAC) system that provides fine-grained access control based on user roles and specific permissions.

### Roles

1. **Admin** - Full system access
2. **Manager** - Most permissions except user management
3. **Cashier** - Limited access focused on sales operations
4. **Stock Manager** - Focused on inventory management

### How RBAC Works

1. **Permission Checking Flow**:
   - First, check if the user has a specific UserPermission assigned
   - If not, check if the user's role has the permission through RolePermission
   - If neither exists, deny access

2. **Two-Level Permission System**:
   - **Role-based permissions**: Defined in `RolePermission` model
   - **User-specific permissions**: Defined in `UserPermission` model for overriding role permissions

### Implementation Details

See [RBAC_IMPLEMENTATION.md](RBAC_IMPLEMENTATION.md) for detailed implementation information.

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up PostgreSQL database
4. Run migrations: `python manage.py migrate`
5. Create default permissions: `python manage.py create_default_permissions`
6. Set up role permissions: `python manage.py setup_permissions`

## Usage

- Access the admin interface at `/admin/`
- Register a new account at `/auth/register/`
- Log in at `/auth/login/`
- View RBAC demo at `/auth/rbac-demo/`
