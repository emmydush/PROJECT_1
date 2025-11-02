# User Role Management

## Overview
This document explains how to manage user roles in the Inventory Management System. User roles determine what parts of the application a user can access.

## User Roles
The system supports the following roles:

1. **admin** - Full access to all system features including settings, user management, and system configuration
2. **manager** - Access to most features except system-level settings
3. **cashier** - Limited access, primarily for sales operations
4. **stock_manager** - Access to inventory management features

## Role-Based Access Control
Certain parts of the application are restricted based on user roles:

- **Settings Module**: Only accessible by users with the "admin" role
- **User Management**: Only accessible by users with the "admin" role
- **Reports**: Access varies by role (admins and managers have full access)

## Managing User Roles

### Using Django Management Commands

#### List All Users
To see all users and their current roles:
```bash
python manage.py list_users
```

#### Update User Role
To change a user's role:
```bash
python manage.py update_user_role <username> <role>
```

Examples:
```bash
# Make a user an admin
python manage.py update_user_role john admin

# Make a user a manager
python manage.py update_user_role jane manager

# Make a user a cashier
python manage.py update_user_role bob cashier

# Make a user a stock manager
python manage.py update_user_role alice stock_manager
```

### Using Django Admin Interface
1. Access the Django admin at `http://localhost:8000/admin/`
2. Navigate to the "Authentication and Authorization" section
3. Click on "Users"
4. Select the user you want to modify
5. Change the "Role" field to the desired role
6. Click "Save"

### Using Django Shell
For more complex operations, you can use the Django shell:

```bash
python manage.py shell
```

Then in the shell:
```python
from authentication.models import User

# Get a user and update their role
user = User.objects.get(username='admin')
user.role = 'admin'
user.save()

# Or update multiple users
User.objects.filter(role='cashier').update(role='manager')
```

## Common Issues and Solutions

### Issue: Redirected to Login When Accessing Settings
**Problem**: When clicking on "Settings" in the navigation menu, you are redirected to the login page.

**Solution**: 
1. Ensure you are logged in as a user with the "admin" role
2. Check the user's role using the `list_users` command
3. If needed, update the user's role using the `update_user_role` command

Example:
```bash
# Check current users
python manage.py list_users

# If your user is not an admin, make them one
python manage.py update_user_role your_username admin
```

### Issue: Insufficient Permissions for Certain Actions
**Problem**: You receive permission denied errors when trying to perform certain actions.

**Solution**:
1. Check your user role using the `list_users` command
2. Request an administrator to update your role if needed
3. Log out and log back in to refresh your permissions

## Best Practices

1. **Principle of Least Privilege**: Assign users the minimum role necessary to perform their job functions
2. **Regular Audits**: Periodically review user roles to ensure they are still appropriate
3. **Role Documentation**: Keep documentation of what each role can access
4. **Admin Accounts**: Limit the number of admin accounts and use them only when necessary

## Troubleshooting

If you continue to have issues accessing restricted areas:

1. Verify you are logged in
2. Check your user role
3. Ensure the URL you're trying to access requires your role level
4. Clear your browser cache and cookies
5. Try logging out and logging back in

For developers:
- Check the view decorators (`@login_required`, `@user_passes_test`)
- Verify the `is_admin` function in settings/views.py
- Confirm LOGIN_URL is properly configured in settings.py