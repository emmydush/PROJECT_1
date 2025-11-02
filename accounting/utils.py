from django.db import transaction, models
from .models import Account, Transaction, TransactionEntry, AccountType

def create_accounting_entry(business, date, description, reference, debit_account, credit_account, amount):
    """
    Create a double-entry accounting transaction.
    
    Args:
        business: The business for which to create the entry
        date: Date of the transaction
        description: Description of the transaction
        reference: Reference number or identifier
        debit_account: Account to debit
        credit_account: Account to credit
        amount: Amount of the transaction
    
    Returns:
        The created Transaction object
    """
    with transaction.atomic():  # type: ignore
        # Create the transaction
        transaction_obj = Transaction.objects.create(
            business=business,
            date=date,
            description=description,
            reference=reference
        )
        
        # Create debit entry
        TransactionEntry.objects.create(
            transaction=transaction_obj,
            account=debit_account,
            business=business,
            amount=amount,
            is_debit=True,
            description=description
        )
        
        # Create credit entry
        TransactionEntry.objects.create(
            transaction=transaction_obj,
            account=credit_account,
            business=business,
            amount=amount,
            is_debit=False,
            description=description
        )
        
        return transaction_obj

def get_or_create_account(business, code, name, account_type, description=""):
    """
    Get or create an account with the specified parameters.
    
    Args:
        business: The business for which to get or create the account
        code: Account code
        name: Account name
        account_type: Type of account (from AccountType)
        description: Description of the account
    
    Returns:
        The Account object and a boolean indicating if it was created
    """
    account, created = Account.objects.get_or_create(
        business=business,
        code=code,
        defaults={
            'name': name,
            'account_type': account_type,
            'description': description
        }
    )
    return account, created

def get_account_balance(account):
    """
    Calculate the balance of an account.
    
    Args:
        account: The Account object
    
    Returns:
        The balance of the account
    """
    # Sum all debit entries
    total_debits = account.entries.filter(is_debit=True).aggregate(
        total=models.Sum('amount')
    )['total'] or 0
    
    # Sum all credit entries
    total_credits = account.entries.filter(is_debit=False).aggregate(
        total=models.Sum('amount')
    )['total'] or 0
    
    # Calculate balance based on account type
    if account.account_type in [AccountType.ASSET, AccountType.EXPENSE]:
        # Assets and expenses increase with debits
        return total_debits - total_credits
    else:
        # Liabilities, equity, and income increase with credits
        return total_credits - total_debits