from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseOrder, PurchaseItem
from products.models import Product

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'expected_delivery_date', 'notes']
        widgets = {
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class PurchaseItemForm(forms.ModelForm):
    # Explicitly define the product field to help static analysis tools
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control product-select'})
    )
    
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control product-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control unit-price-input', 'step': '0.01'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the product field has the correct class
        self.fields['product'].widget.attrs.update({'class': 'form-control product-select'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['unit_price'].widget.attrs.update({'class': 'form-control unit-price-input'})

PurchaseItemFormSet = inlineformset_factory(
    PurchaseOrder, PurchaseItem,
    form=PurchaseItemForm,
    extra=3,  # Show 3 empty forms by default
    can_delete=True
)