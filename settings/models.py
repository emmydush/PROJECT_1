from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

class BusinessSettings(models.Model):
    business_name = models.CharField(max_length=200, default='Smart Solution')
    business_address = models.TextField(default='123 Business Street, City, Country')
    business_email = models.EmailField(default='info@smartsolution.com')
    business_phone = models.CharField(max_length=20, default='+1 (555) 123-4567')
    business_logo = models.ImageField(upload_to='business/logo/', blank=True, null=True)
    currency = models.CharField(max_length=3, default='FRW')
    currency_symbol = models.CharField(max_length=10, default='FRW')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # Expiry alert settings
    expiry_alert_days = models.IntegerField(default=7, help_text='Number of days before expiry to send alerts')  # type: ignore
    near_expiry_alert_days = models.IntegerField(default=30, help_text='Number of days before expiry to send near expiry alerts')  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Business Settings"

    def __str__(self) -> str:  # type: ignore
        return self.business_name  # type: ignore

class BarcodeSettings(models.Model):
    BARCODE_TYPES = (
        ('CODE128', 'Code 128'),
        ('CODE39', 'Code 39'),
        ('EAN13', 'EAN-13'),
        ('UPC-A', 'UPC-A'),
    )
    
    barcode_type = models.CharField(max_length=10, choices=BARCODE_TYPES, default='CODE128')
    barcode_width = models.IntegerField(default=200)  # type: ignore
    barcode_height = models.IntegerField(default=100)  # type: ignore
    display_text = models.BooleanField(default=True)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Barcode Settings"

    def __str__(self) -> str:  # type: ignore
        return f"{self.barcode_type} Settings"  # type: ignore

class EmailSettings(models.Model):
    EMAIL_BACKEND_CHOICES = (
        ('django.core.mail.backends.smtp.EmailBackend', 'SMTP (Gmail, SendGrid, etc.)'),
        ('django.core.mail.backends.console.EmailBackend', 'Console (Development - Print to Terminal)'),
        ('django_ses.SESBackend', 'Amazon SES'),
    )
    
    email_backend = models.CharField(max_length=100, choices=EMAIL_BACKEND_CHOICES, default='django.core.mail.backends.smtp.EmailBackend')
    email_host = models.CharField(max_length=100, blank=True, null=True, help_text='SMTP server address (e.g., smtp.gmail.com)')
    email_port = models.IntegerField(default=587, help_text='SMTP port (587 for TLS, 465 for SSL)')  # type: ignore
    email_host_user = models.CharField(max_length=100, blank=True, null=True, help_text='Email address or username')
    email_host_password = models.CharField(max_length=100, blank=True, null=True, help_text='Password or app password')
    email_use_tls = models.BooleanField(default=True, help_text='Use TLS encryption')  # type: ignore
    email_use_ssl = models.BooleanField(default=False, help_text='Use SSL encryption')  # type: ignore
    default_from_email = models.CharField(max_length=100, default='Inventory Management System <webmaster@localhost>', help_text='Default sender email address')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Email Settings"

    def __str__(self) -> str:  # type: ignore
        return "Email Configuration"  # type: ignore