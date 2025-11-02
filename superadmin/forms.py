from django import forms
from .models import Business

class BusinessDetailsForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['company_name', 'email', 'business_type']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'business_type': forms.Select(attrs={'class': 'form-select'}),
        }