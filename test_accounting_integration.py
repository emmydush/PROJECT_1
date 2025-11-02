import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

# Now we can import Django models
from sales.models import Sale
from customers.models import Customer
from superadmin.models import Business
from expenses.models import Expense, ExpenseCategory
from decimal import Decimal
from django.utils import timezone

# Get the first business and customer
business = Business.objects.first()
print(f"Business: {business}")

if business:
    # Set the current business context (this is usually done by middleware)
    from superadmin.middleware import set_current_business
    set_current_business(business)
    
    # Test sale integration
    customer = Customer.objects.business_specific().first()
    print(f"Customer: {customer}")
    
    if customer:
        # Create a sale
        sale = Sale.objects.create(
            business=business,
            customer=customer,
            subtotal=Decimal('100'),
            tax=Decimal('10'),
            total_amount=Decimal('110'),
            payment_method='cash'
        )
        print(f"Created sale: {sale}")
        
        # Check if accounting entries were created
        from accounting.models import Transaction, TransactionEntry
        transactions = Transaction.objects.business_specific().filter(reference=f"Sale-{sale.pk}")
        print(f"Accounting transactions created for sale: {transactions.count()}")
        
        for transaction in transactions:
            entries = transaction.entries.all()
            print(f"Transaction {transaction}:")
            for entry in entries:
                print(f"  {entry}")
    
    # Test expense integration
    # Create an expense category if it doesn't exist
    category, created = ExpenseCategory.objects.get_or_create(
        business=business,
        name="Office Supplies"
    )
    print(f"Expense category: {category}")
    
    # Create an expense
    expense = Expense.objects.create(
        business=business,
        category=category,
        amount=Decimal('50.00'),
        date=timezone.now().date(),
        description="Printer ink cartridges"
    )
    print(f"Created expense: {expense}")
    
    # Check if accounting entries were created
    from accounting.models import Transaction, TransactionEntry
    expense_transactions = Transaction.objects.business_specific().filter(reference=f"Expense-{expense.pk}")
    print(f"Accounting transactions created for expense: {expense_transactions.count()}")
    
    for transaction in expense_transactions:
        entries = transaction.entries.all()
        print(f"Transaction {transaction}:")
        for entry in entries:
            print(f"  {entry}")
else:
    print("No business found")