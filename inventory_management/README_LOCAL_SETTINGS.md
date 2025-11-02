# Local Settings Configuration

This document explains how to configure your local settings for email and other sensitive information.

## Email Configuration

1. The system uses `local_settings.py` to store sensitive information like email credentials.
2. This file is excluded from version control for security reasons.

## Setup Instructions

1. Open `local_settings.py` in this directory
2. Replace the placeholder values with your actual credentials:
   - `EMAIL_HOST_USER`: Your Gmail address
   - `EMAIL_HOST_PASSWORD`: Your Gmail app password (not your regular password)
   - `DEFAULT_FROM_EMAIL`: Your Gmail address in the format "Display Name <email@example.com>"

## Example Configuration

```python
# Gmail Configuration
EMAIL_HOST_USER = 'youremail@gmail.com'  # Your actual Gmail address
EMAIL_HOST_PASSWORD = 'srin jitw qwpy gaaz'  # Your app password from Google
DEFAULT_FROM_EMAIL = 'Inventory Management System <youremail@gmail.com>'  # Your Gmail address
```

## Security Notes

1. Never commit `local_settings.py` to version control
2. The `.gitignore` file should exclude this file
3. For production environments, consider using environment variables instead

## Testing Email Configuration

After updating your local settings, you can test the email configuration by running:

```bash
python manage.py send_expiry_emails
```

This will send test emails to verify your configuration is working correctly.