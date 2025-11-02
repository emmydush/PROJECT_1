from django.core.management.base import BaseCommand
from superadmin.models import Business
from accounting.models import Account, AccountType

class Command(BaseCommand):
    help = 'Create default chart of accounts for all businesses'

    def handle(self, *args, **options):
        # Default accounts to create
        default_accounts = [
            # Assets
            {'code': '1000', 'name': 'Cash', 'account_type': AccountType.ASSET, 'description': 'Cash on hand and in bank accounts'},
            {'code': '1100', 'name': 'Accounts Receivable', 'account_type': AccountType.ASSET, 'description': 'Money owed by customers'},
            {'code': '1200', 'name': 'Inventory', 'account_type': AccountType.ASSET, 'description': 'Products available for sale'},
            {'code': '1300', 'name': 'Prepaid Expenses', 'account_type': AccountType.ASSET, 'description': 'Expenses paid in advance'},
            {'code': '1400', 'name': 'Equipment', 'account_type': AccountType.ASSET, 'description': 'Business equipment and machinery'},
            {'code': '1500', 'name': 'Accumulated Depreciation', 'account_type': AccountType.ASSET, 'description': 'Depreciation on equipment'},
            
            # Liabilities
            {'code': '2000', 'name': 'Accounts Payable', 'account_type': AccountType.LIABILITY, 'description': 'Money owed to suppliers'},
            {'code': '2100', 'name': 'Notes Payable', 'account_type': AccountType.LIABILITY, 'description': 'Loans and notes payable'},
            {'code': '2200', 'name': 'Accrued Expenses', 'account_type': AccountType.LIABILITY, 'description': 'Expenses incurred but not yet paid'},
            {'code': '2300', 'name': 'Taxes Payable', 'account_type': AccountType.LIABILITY, 'description': 'Taxes owed to government'},
            
            # Equity
            {'code': '3000', 'name': 'Owner\'s Equity', 'account_type': AccountType.EQUITY, 'description': 'Owner\'s investment in the business'},
            {'code': '3100', 'name': 'Retained Earnings', 'account_type': AccountType.EQUITY, 'description': 'Accumulated profits'},
            
            # Income
            {'code': '4000', 'name': 'Sales Revenue', 'account_type': AccountType.INCOME, 'description': 'Revenue from sales of products'},
            {'code': '4100', 'name': 'Service Revenue', 'account_type': AccountType.INCOME, 'description': 'Revenue from services provided'},
            {'code': '4200', 'name': 'Other Income', 'account_type': AccountType.INCOME, 'description': 'Other sources of income'},
            
            # Expenses
            {'code': '5000', 'name': 'Cost of Goods Sold', 'account_type': AccountType.EXPENSE, 'description': 'Direct costs of products sold'},
            {'code': '5100', 'name': 'Salaries and Wages', 'account_type': AccountType.EXPENSE, 'description': 'Employee compensation'},
            {'code': '5200', 'name': 'Rent Expense', 'account_type': AccountType.EXPENSE, 'description': 'Rent for business premises'},
            {'code': '5300', 'name': 'Utilities Expense', 'account_type': AccountType.EXPENSE, 'description': 'Electricity, water, gas, etc.'},
            {'code': '5400', 'name': 'Marketing Expense', 'account_type': AccountType.EXPENSE, 'description': 'Advertising and marketing costs'},
            {'code': '5500', 'name': 'Insurance Expense', 'account_type': AccountType.EXPENSE, 'description': 'Business insurance premiums'},
            {'code': '5600', 'name': 'Depreciation Expense', 'account_type': AccountType.EXPENSE, 'description': 'Depreciation on equipment'},
            {'code': '5700', 'name': 'Office Supplies', 'account_type': AccountType.EXPENSE, 'description': 'Office supplies and materials'},
            {'code': '5800', 'name': 'Professional Fees', 'account_type': AccountType.EXPENSE, 'description': 'Legal, accounting, and consulting fees'},
            {'code': '5900', 'name': 'Miscellaneous Expense', 'account_type': AccountType.EXPENSE, 'description': 'Other business expenses'},
        ]
        
        businesses = Business.objects.all()
        
        accounts_created = 0
        accounts_skipped = 0
        
        for business in businesses:
            self.stdout.write(f'Creating accounts for business: {business.company_name}')
            
            for account_data in default_accounts:
                try:
                    # Check if account already exists for this business
                    if not Account.objects.filter(
                        business=business,
                        code=account_data['code']
                    ).exists():
                        # Create the account for this business
                        Account.objects.create(
                            business=business,
                            code=account_data['code'],
                            name=account_data['name'],
                            account_type=account_data['account_type'],
                            description=account_data['description']
                        )
                        accounts_created += 1
                    else:
                        accounts_skipped += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Failed to create account {account_data["code"]} for business {business.company_name}: {str(e)}'
                        )
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {accounts_created} accounts. '
                f'Skipped {accounts_skipped} existing accounts.'
            )
        )