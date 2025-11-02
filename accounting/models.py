from django.db import models
from superadmin.models import Business
from superadmin.managers import BusinessSpecificManager

class AccountType(models.TextChoices):
    ASSET = 'asset', 'Asset'
    LIABILITY = 'liability', 'Liability'
    EQUITY = 'equity', 'Equity'
    INCOME = 'income', 'Income'
    EXPENSE = 'expense', 'Expense'

class Account(models.Model):
    """Represents a general ledger account"""
    objects = BusinessSpecificManager()
    
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        unique_together = ('business', 'code')

    def __str__(self):
        return f"{self.code} - {self.name}"

class Transaction(models.Model):
    """Represents a financial transaction (debit/credit entry)"""
    objects = BusinessSpecificManager()
    
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    description = models.CharField(max_length=200)
    reference = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.date} - {self.description}"

class TransactionEntry(models.Model):
    """Represents a debit or credit entry in a transaction"""
    objects = BusinessSpecificManager()
    
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='entries')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='entries')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='transaction_entries')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    is_debit = models.BooleanField(default=True)  # type: ignore
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        entry_type = "Dr" if self.is_debit else "Cr"
        return f"{entry_type} {self.account.name} ${self.amount}"

    @property
    def entry_type(self):
        return "Debit" if self.is_debit else "Credit"