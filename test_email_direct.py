import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('E:/AI')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartbusiness.settings')

# Setup Django
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("Current email settings:")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

try:
    print("Sending test email...")
    send_mail(
        'Test Email from Smart Business System',
        'This is a test email to verify that the email configuration is working correctly.',
        settings.DEFAULT_FROM_EMAIL,
        ['emmychris915@gmail.com'],
        fail_silently=False,
    )
    print("Test email sent successfully!")
except Exception as e:
    print(f"Failed to send test email: {e}")