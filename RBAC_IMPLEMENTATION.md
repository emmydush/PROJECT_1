# Role-Based Access Control (RBAC) Implementation

This document explains how the Role-Based Access Control (RBAC) system is implemented in the Inventory Management System.

## Overview

The RBAC system provides fine-grained access control based on user roles and specific permissions. Instead of universal access, users are granted access based on their role and specific permissions assigned to them.

## Components

### 1. User Model
The [User](file:///E:/AI/authentication/models.py#L4-L31) model extends Django's `AbstractUser` and includes:
- `role`: Defines the user's role (admin, manager, cashier, stock_manager)
- `businesses`: Many-to-many relationship with businesses
- `has_custom_permission()`: Method to check if a user has a specific permission

### 2. Permission Model
The [Permission](file:///E:/AI/authentication/models.py#L34-L46) model defines system permissions:
- `name`: Unique permission identifier
- `description`: Human-readable description
- `category`: Grouping category for permissions

### 3. RolePermission Model
The [RolePermission](file:///E:/AI/authentication/models.py#L48-L61) model links roles to permissions:
- `role`: User role
- `permission`: Permission assigned to the role

### 4. UserPermission Model
The [UserPermission](file:///E:/AI/authentication/models.py#L63-L80) model allows assigning specific permissions to individual users:
- `user`: Target user
- `permission`: Permission to assign
- `granted`: Whether the permission is granted or denied

## Permission Checking Flow

When checking if a user has a permission:
1. First, check if the user has a specific UserPermission assigned
2. If not, check if the user's role has the permission through RolePermission
3. If neither exists, deny access

## Usage Examples

### In Views
```python
from authentication.decorators import permission_required, role_required

# Restrict access to users with specific permission
@permission_required('view_products')
def product_list_view(request):
    # View logic here
    pass

# Restrict access to specific roles
@role_required(['admin', 'manager'])
def manage_users_view(request):
    # View logic here
    pass
```

### Programmatic Checking
```python
# Check permission in view logic
if request.user.has_custom_permission('edit_products'):
    # Allow editing
    pass
else:
    # Deny access
    pass
```

## Management Commands

### Create Default Permissions
```bash
python manage.py create_default_permissions
```

### Set Up Role Permissions
```bash
python manage.py setup_permissions
```

### Test Permissions
```bash
python manage.py test_permissions
```

## Role Definitions

1. **Admin**: Full system access
2. **Manager**: Most permissions except user management
3. **Cashier**: Limited access focused on sales operations
4. **Stock Manager**: Focused on inventory management

## Benefits

1. **Granular Control**: Permissions can be assigned at both role and user levels
2. **Flexibility**: Users can have permissions beyond their role
3. **Security**: Default deny policy ensures only explicitly granted permissions are allowed
4. **Scalability**: Easy to add new roles and permissions as needed