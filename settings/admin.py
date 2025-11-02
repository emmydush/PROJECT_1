from django.contrib import admin
from .models import BusinessSettings, BarcodeSettings, EmailSettings

@admin.register(BusinessSettings)
class BusinessSettingsAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'business_email', 'business_phone', 'currency')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Business Information', {
            'fields': ('business_name', 'business_address', 'business_email', 'business_phone', 'business_logo')
        }),
        ('Currency Settings', {
            'fields': ('currency', 'currency_symbol', 'tax_rate')
        }),
        ('Expiry Alert Settings', {
            'fields': ('expiry_alert_days', 'near_expiry_alert_days')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(BarcodeSettings)
class BarcodeSettingsAdmin(admin.ModelAdmin):
    list_display = ('barcode_type', 'barcode_width', 'barcode_height', 'display_text')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Barcode Configuration', {
            'fields': ('barcode_type', 'barcode_width', 'barcode_height', 'display_text')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ('email_backend', 'email_host', 'email_host_user')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Email Backend', {
            'fields': ('email_backend',)
        }),
        ('SMTP Settings', {
            'fields': ('email_host', 'email_port', 'email_host_user', 'email_host_password', 'email_use_tls', 'email_use_ssl')
        }),
        ('Sender Information', {
            'fields': ('default_from_email',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )