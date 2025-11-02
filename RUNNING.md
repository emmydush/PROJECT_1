# Running the Inventory Management System

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone or download the repository
2. Navigate to the project directory:
   ```
   cd inventory_management
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Database Setup

1. Run migrations to create the database schema:
   ```
   python manage.py migrate
   ```

2. Create a superuser account:
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.

3. (Optional) Initialize the database with sample data:
   ```
   python manage.py init_data
   ```

## Setting Up Scheduled Tasks

The system includes automatic expiry date alerts that should run daily. See [SCHEDULED_TASKS.md](SCHEDULED_TASKS.md) for detailed instructions on setting up scheduled tasks.

Essential commands to run daily:
- `python manage.py generate_notifications` - Creates in-app notifications
- `python manage.py send_expiry_emails` - Sends email alerts for expiry dates

## Configuring Email Settings

### For Development
The system uses the console email backend by default, which prints emails to the terminal. This is useful for development and testing.

### For Gmail (Production)
To configure Gmail for sending real emails:

1. Create a `local_settings.py` file in the `inventory_management` directory
2. Add your Gmail configuration:
   ```python
   # Gmail Configuration
   EMAIL_HOST_USER = 'your-email@gmail.com'  # Your actual Gmail address
   EMAIL_HOST_PASSWORD = 'your-app-password'  # Your Gmail app password
   DEFAULT_FROM_EMAIL = 'Inventory Management System <your-email@gmail.com>'  # Your Gmail address
   ```

3. Generate an App Password for Gmail:
   - Go to your Google Account settings
   - Navigate to Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this app password in your configuration (not your regular Gmail password)

4. Test your configuration:
   ```
   python test_gmail.py
   ```

### For Other Email Providers
For other providers, see [SCHEDULED_TASKS.md](SCHEDULED_TASKS.md) for detailed configuration instructions.

## Running the Application

1. Start the development server:
   ```
   python manage.py runserver
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

3. You will be automatically redirected to the login page. Login with your superuser credentials or the default admin user:
   - Username: admin
   - Password: admin123

## Testing the Application

To run the test script:
```
python test_app.py
```

To test email configuration:
```
python test_gmail.py
```

To test expiry notifications:
```
python manage.py send_expiry_emails
```

## Application Structure

The application is organized into the following modules:

- **Authentication**: User management and authentication
- **Dashboard**: Main dashboard with overview statistics
- **Products**: Product and inventory management
- **Suppliers**: Supplier management
- **Purchases**: Purchase order management
- **Sales**: Sales and POS system
- **Customers**: Customer management
- **Expenses**: Expense tracking
- **Reports**: Business reporting and analytics
- **Notifications**: System notifications and alerts
- **Settings**: System configuration and settings

## Features

- User authentication with role-based access control
- Product inventory management with low stock alerts
- Supplier and customer management
- Purchase order and sales management
- Expense tracking
- Financial reporting
- Responsive web interface
- Data export capabilities
- Expiry date tracking with automatic alerts
- Email notifications for urgent alerts
- Personal inventory alerts sent directly to business email

## Customization

To customize the application for your specific needs:

1. Modify the templates in the `templates/` directory
2. Update the models in the respective app directories
3. Adjust the views and forms as needed
4. Update the static files (CSS, JavaScript) in the `static/` directory

## Production Deployment

For production deployment, consider:

1. Using PostgreSQL instead of SQLite
2. Setting up a proper web server (nginx, Apache)
3. Configuring SSL certificates
4. Setting up environment variables for sensitive data
5. Using a production WSGI server (Gunicorn, uWSGI)
6. Implementing proper backup and monitoring solutions
7. Setting up scheduled tasks for automatic notifications
8. Configuring email settings for alert notifications
9. Using environment variables for email credentials instead of hardcoding them

## Troubleshooting

### Common Issues

1. **Database connection errors**: Ensure your database is running and the connection settings in `settings.py` are correct.

2. **Missing migrations**: Run `python manage.py makemigrations` followed by `python manage.py migrate`.

3. **Static files not loading**: Run `python manage.py collectstatic` in production.

4. **Permission errors**: Ensure the user running the application has proper permissions for the project directory.

5. **Email notifications not working**: Check email configuration in `inventory_management/local_settings.py` and ensure scheduled tasks are set up.

6. **Gmail authentication issues**: 
   - Ensure you're using an App Password, not your regular Gmail password
   - Check that 2-Factor Authentication is enabled
   - Verify that the Gmail account allows SMTP access

### Getting Help

For additional help, refer to the Django documentation or contact the development team.