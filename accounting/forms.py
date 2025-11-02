from django import forms
from .models import Account, Transaction, TransactionEntry

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'code', 'account_type', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'description', 'reference']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class TransactionEntryForm(forms.ModelForm):
    class Meta:
        model = TransactionEntry
        fields = ['account', 'amount', 'is_debit', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }