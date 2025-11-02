from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Account, TransactionEntry, AccountType
from settings.models import BusinessSettings

@login_required
def accounting_index(request):
    """Main index page for the accounting section"""
    # Get business settings
    business_settings, created = BusinessSettings.objects.get_or_create(id=1)
    
    context = {
        'business_settings': business_settings,
    }
    
    return render(request, 'accounting/index.html', context)


@login_required
def income_statement(request):
    """Display the income statement (profit and loss report)"""
    # Get business settings for currency and business name
    business_settings, created = BusinessSettings.objects.get_or_create(id=1)
    
    # Get income accounts and their totals
    income_accounts = Account.objects.business_specific().filter(account_type=AccountType.INCOME)
    income_details = []
    total_income = 0
    
    for account in income_accounts:
        # Sum all credit entries (income increases with credits)
        total = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Subtract debit entries (income decreases with debits)
        debits = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        net_amount = total - debits
        
        if net_amount != 0:  # Only show accounts with activity
            income_details.append({
                'account': account,
                'amount': net_amount
            })
            total_income += net_amount
    
    # Get expense accounts and their totals
    expense_accounts = Account.objects.business_specific().filter(account_type=AccountType.EXPENSE)
    expense_details = []
    total_expenses = 0
    
    for account in expense_accounts:
        # Sum all debit entries (expenses increase with debits)
        total = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Subtract credit entries (expenses decrease with credits)
        credits = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        net_amount = total - credits
        
        if net_amount != 0:  # Only show accounts with activity
            expense_details.append({
                'account': account,
                'amount': net_amount
            })
            total_expenses += net_amount
    
    # Calculate net profit/loss
    net_profit = total_income - total_expenses
    
    context = {
        'income_details': income_details,
        'total_income': total_income,
        'expense_details': expense_details,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'business_settings': business_settings,
    }
    
    return render(request, 'accounting/reports/income_statement.html', context)


@login_required
def balance_sheet(request):
    """Display the balance sheet report"""
    # Get business settings for currency and business name
    business_settings, created = BusinessSettings.objects.get_or_create(id=1)
    
    # Get asset accounts and their totals
    asset_accounts = Account.objects.business_specific().filter(account_type=AccountType.ASSET)
    asset_details = []
    total_assets = 0
    
    for account in asset_accounts:
        # Sum all debit entries (assets increase with debits)
        debits = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Subtract credit entries (assets decrease with credits)
        credits = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        net_amount = debits - credits
        
        if net_amount != 0:  # Only show accounts with activity
            asset_details.append({
                'account': account,
                'amount': net_amount
            })
            total_assets += net_amount
    
    # Get liability accounts and their totals
    liability_accounts = Account.objects.business_specific().filter(account_type=AccountType.LIABILITY)
    liability_details = []
    total_liabilities = 0
    
    for account in liability_accounts:
        # Sum all credit entries (liabilities increase with credits)
        credits = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Subtract debit entries (liabilities decrease with debits)
        debits = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        net_amount = credits - debits
        
        if net_amount != 0:  # Only show accounts with activity
            liability_details.append({
                'account': account,
                'amount': net_amount
            })
            total_liabilities += net_amount
    
    # Get equity accounts and their totals
    equity_accounts = Account.objects.business_specific().filter(account_type=AccountType.EQUITY)
    equity_details = []
    total_equity = 0
    
    for account in equity_accounts:
        # Sum all credit entries (equity increases with credits)
        credits = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Subtract debit entries (equity decreases with debits)
        debits = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        net_amount = credits - debits
        
        if net_amount != 0:  # Only show accounts with activity
            equity_details.append({
                'account': account,
                'amount': net_amount
            })
            total_equity += net_amount
    
    # Calculate net profit/loss from income statement to include in equity
    # This is a simplified approach - in a real system, you might want to get this from a retained earnings account
    income_accounts = Account.objects.business_specific().filter(account_type=AccountType.INCOME)
    expense_accounts = Account.objects.business_specific().filter(account_type=AccountType.EXPENSE)
    
    total_income = 0
    for account in income_accounts:
        # Sum all credit entries (income increases with credits)
        total = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Subtract debit entries (income decreases with debits)
        debits = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        net_amount = total - debits
        total_income += net_amount
    
    total_expenses = 0
    for account in expense_accounts:
        # Sum all debit entries (expenses increase with debits)
        total = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=True
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Subtract credit entries (expenses decrease with credits)
        credits = TransactionEntry.objects.business_specific().filter(
            account=account, 
            is_debit=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        net_amount = total - credits
        total_expenses += net_amount
    
    net_profit = total_income - total_expenses
    
    # Add net profit to equity total
    total_equity += net_profit
    
    context = {
        'asset_details': asset_details,
        'total_assets': total_assets,
        'liability_details': liability_details,
        'total_liabilities': total_liabilities,
        'equity_details': equity_details,
        'total_equity': total_equity,
        'net_profit': net_profit,
        'business_settings': business_settings,
    }
    
    return render(request, 'accounting/reports/balance_sheet.html', context)
