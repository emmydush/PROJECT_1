from django import forms
from .models import Expense, ExpenseCategory
from superadmin.middleware import get_current_business

class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the current business from middleware
        current_business = get_current_business()
        if current_business:
            # Filter categories by current business
            self.fields['category'].queryset = ExpenseCategory.objects.filter(business=current_business)
        else:
            # If no business context, show all categories (fallback)
            self.fields['category'].queryset = ExpenseCategory.objects.all()
    
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }