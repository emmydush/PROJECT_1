from django import forms
from .models import BusinessSettings, BarcodeSettings, EmailSettings

class BusinessSettingsForm(forms.ModelForm):
    class Meta:
        model = BusinessSettings
        fields = ['business_name', 'business_address', 'business_email', 'business_phone', 
                  'business_logo', 'currency', 'currency_symbol', 'tax_rate', 
                  'expiry_alert_days', 'near_expiry_alert_days']
        widgets = {
            'business_address': forms.Textarea(attrs={'rows': 3}),
            'expiry_alert_days': forms.NumberInput(attrs={'min': 1}),
            'near_expiry_alert_days': forms.NumberInput(attrs={'min': 1}),
            'tax_rate': forms.NumberInput(attrs={'step': '0.01'}),
        }

class BarcodeSettingsForm(forms.ModelForm):
    class Meta:
        model = BarcodeSettings
        fields = ['barcode_type', 'barcode_width', 'barcode_height', 'display_text']
        widgets = {
            'barcode_width': forms.NumberInput(attrs={'min': 50}),
            'barcode_height': forms.NumberInput(attrs={'min': 50}),
        }

class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = ['email_backend', 'email_host', 'email_port', 'email_host_user', 
                  'email_host_password', 'email_use_tls', 'email_use_ssl', 'default_from_email']
        widgets = {
            'email_host_password': forms.PasswordInput(render_value=True),
            'email_port': forms.NumberInput(attrs={'min': 1, 'max': 65535}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text for common email providers
        self.fields['email_host'].help_text = "SMTP server address (e.g., smtp.gmail.com for Gmail, smtp.sendgrid.net for SendGrid)"
        self.fields['email_host_user'].help_text = "Email address or username (for Gmail, use your full email address)"
        self.fields['email_host_password'].help_text = "Password or app password (for Gmail, use an App Password)"
        
        # Set initial values based on current settings
        if not self.instance.pk:  # If creating new instance
            self.fields['email_host'].initial = 'smtp.gmail.com'
            self.fields['email_port'].initial = 587
            self.fields['email_use_tls'].initial = True
            self.fields['email_use_ssl'].initial = False
    
    def clean(self):
        cleaned_data = super().clean()
        email_backend = cleaned_data.get('email_backend')
        email_host = cleaned_data.get('email_host')
        email_host_user = cleaned_data.get('email_host_user')
        
        # Validate SMTP settings if using SMTP backend
        if email_backend == 'django.core.mail.backends.smtp.EmailBackend':
            if not email_host:
                self.add_error('email_host', 'Email host is required for SMTP backend.')
            if not email_host_user:
                self.add_error('email_host_user', 'Email host user is required for SMTP backend.')
        
        # Validate TLS/SSL settings
        email_use_tls = cleaned_data.get('email_use_tls')
        email_use_ssl = cleaned_data.get('email_use_ssl')
        
        if email_use_tls and email_use_ssl:
            raise forms.ValidationError('Only one of TLS or SSL can be enabled, not both.')
            
        return cleaned_data