from django import forms
from .models import Business, Branch
from django.contrib.auth import get_user_model

User = get_user_model()

class BusinessRegistrationForm(forms.ModelForm):
    owner_email = forms.EmailField(
        label="Owner Email",
        help_text="Email of the business owner"
    )
    
    class Meta:
        model = Business
        fields = ['company_name', 'email', 'business_type']
        labels = {
            'company_name': 'Company Name',
            'email': 'Business Email',
            'business_type': 'Business Type',
        }
        help_texts = {
            'company_name': 'Enter the official name of your company',
            'email': 'Enter the main business email address',
            'business_type': 'Select the type of business',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['business_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['owner_email'].widget.attrs.update({'class': 'form-control'})

    def clean_owner_email(self):
        owner_email = self.cleaned_data.get('owner_email')
        if User.objects.filter(email=owner_email).exists():
            raise forms.ValidationError("A user with this email already exists. Please use a different email or log in.")
        return owner_email

    def save(self, commit=True):
        business = super().save(commit=False)
        # Set default values
        business.plan_type = 'free'
        business.status = 'pending'
        
        if commit:
            business.save()
        return business

class BusinessDetailsForm(forms.ModelForm):
    """Form for users to enter their business details after registration"""
    
    class Meta:
        model = Business
        fields = ['company_name', 'email', 'business_type']
        labels = {
            'company_name': 'Company Name',
            'email': 'Business Email',
            'business_type': 'Business Type',
        }
        help_texts = {
            'company_name': 'Enter the official name of your company',
            'email': 'Enter the main business email address',
            'business_type': 'Select the type of business',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['business_type'].widget.attrs.update({'class': 'form-select'})

class BranchForm(forms.ModelForm):
    """Form for creating and updating branches"""
    
    class Meta:
        model = Branch
        fields = ['name', 'address', 'phone', 'email', 'manager', 'is_main', 'is_active']
        labels = {
            'name': 'Branch Name',
            'address': 'Branch Address',
            'phone': 'Phone Number',
            'email': 'Email Address',
            'manager': 'Branch Manager',
            'is_main': 'Main Branch',
            'is_active': 'Active',
        }
        help_texts = {
            'name': 'Enter the name of the branch',
            'address': 'Enter the full address of the branch',
            'phone': 'Enter the phone number for this branch',
            'email': 'Enter the email address for this branch',
            'manager': 'Select a manager for this branch',
            'is_main': 'Mark this as the main branch of your business',
            'is_active': 'Uncheck to deactivate this branch',
        }

    def __init__(self, *args, **kwargs):
        # Extract business from kwargs if provided
        business = kwargs.pop('business', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['manager'].widget.attrs.update({'class': 'form-select'})
        self.fields['is_main'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        
        # Add help text for is_main field
        self.fields['is_main'].help_text = "Mark this as the main branch of your business"
        self.fields['is_active'].help_text = "Uncheck to deactivate this branch"
        
        # Filter managers to only include users from the current business
        if business:
            self.fields['manager'].queryset = User.objects.filter(businesses=business)
        elif self.instance and self.instance.pk:
            # If editing an existing branch, filter by the branch's business
            self.fields['manager'].queryset = User.objects.filter(businesses=self.instance.business)
