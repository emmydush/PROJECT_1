from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from sales.models import Sale, SaleItem
from purchases.models import PurchaseOrder, PurchaseItem
from expenses.models import Expense
from .models import Account, Transaction, TransactionEntry, AccountType
import logging

# Set up logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Sale)
def create_sale_accounting_entries(sender, instance, created, **kwargs):
    """
    Create accounting entries when a sale is made.
    Debit: Cash/Bank Account (Asset)
    Credit: Sales Revenue Account (Income)
    """
    if created and not instance.is_refunded:
        try:
            with transaction.atomic():
                # Get or create the necessary accounts
                business = instance.business
                
                # Determine which asset account to use based on payment method
                if instance.payment_method == 'cash':
                    asset_account, _ = Account.objects.get_or_create(
                        business=business,
                        code='1000',
                        defaults={
                            'name': 'Cash',
                            'account_type': AccountType.ASSET,
                            'description': 'Cash on hand'
                        }
                    )
                else:
                    asset_account, _ = Account.objects.get_or_create(
                        business=business,
                        code='1001',
                        defaults={
                            'name': 'Bank',
                            'account_type': AccountType.ASSET,
                            'description': 'Bank account'
                        }
                    )
                
                # Get or create sales revenue account
                revenue_account, _ = Account.objects.get_or_create(
                    business=business,
                    code='4000',
                    defaults={
                        'name': 'Sales Revenue',
                        'account_type': AccountType.INCOME,
                        'description': 'Revenue from sales'
                    }
                )
                
                # Create the transaction
                transaction_obj = Transaction.objects.create(
                    business=business,
                    date=instance.sale_date.date(),
                    description=f"Sale #{instance.pk}",
                    reference=f"Sale-{instance.pk}"
                )
                
                # Create debit entry (increase in asset)
                TransactionEntry.objects.create(
                    transaction=transaction_obj,
                    account=asset_account,
                    business=business,
                    amount=instance.total_amount,
                    is_debit=True,
                    description=f"Payment received for Sale #{instance.pk}"
                )
                
                # Create credit entry (increase in revenue)
                TransactionEntry.objects.create(
                    transaction=transaction_obj,
                    account=revenue_account,
                    business=business,
                    amount=instance.total_amount,
                    is_debit=False,
                    description=f"Sales revenue for Sale #{instance.pk}"
                )
                
        except Exception as e:
            logger.error(f"Error creating accounting entries for sale {instance.pk}: {str(e)}")

@receiver(post_save, sender=PurchaseOrder)
def create_purchase_accounting_entries(sender, instance, created, **kwargs):
    """
    Create accounting entries when a purchase order is created.
    Debit: Inventory/Purchase Account (Asset/Expense)
    Credit: Accounts Payable/Cash/Bank Account (Liability/Asset)
    """
    if created:
        try:
            with transaction.atomic():
                business = instance.business
                
                # Get or create inventory account
                inventory_account, _ = Account.objects.get_or_create(
                    business=business,
                    code='1200',
                    defaults={
                        'name': 'Inventory',
                        'account_type': AccountType.ASSET,
                        'description': 'Inventory of goods'
                    }
                )
                
                # Determine which account to credit based on payment terms
                # For now, we'll assume accounts payable for all purchases
                liability_account, _ = Account.objects.get_or_create(
                    business=business,
                    code='2000',
                    defaults={
                        'name': 'Accounts Payable',
                        'account_type': AccountType.LIABILITY,
                        'description': 'Amounts owed to suppliers'
                    }
                )
                
                # Create the transaction
                transaction_obj = Transaction.objects.create(
                    business=business,
                    date=instance.order_date.date(),
                    description=f"Purchase Order #{instance.pk}",
                    reference=f"PO-{instance.pk}"
                )
                
                # Create debit entry (increase in inventory/asset)
                TransactionEntry.objects.create(
                    transaction=transaction_obj,
                    account=inventory_account,
                    business=business,
                    amount=instance.total_amount,
                    is_debit=True,
                    description=f"Inventory purchase for PO #{instance.pk}"
                )
                
                # Create credit entry (increase in liability)
                TransactionEntry.objects.create(
                    transaction=transaction_obj,
                    account=liability_account,
                    business=business,
                    amount=instance.total_amount,
                    is_debit=False,
                    description=f"Accounts payable for PO #{instance.pk}"
                )
                
        except Exception as e:
            logger.error(f"Error creating accounting entries for purchase order {instance.pk}: {str(e)}")

@receiver(post_save, sender=Expense)
def create_expense_accounting_entries(sender, instance, created, **kwargs):
    """
    Create accounting entries when an expense is recorded.
    Debit: Expense Account (Expense)
    Credit: Cash/Bank Account (Asset)
    """
    if created:
        try:
            with transaction.atomic():
                business = instance.business
                
                # Get or create the expense account
                expense_account, _ = Account.objects.get_or_create(
                    business=business,
                    code=f'6000-{instance.category.id}',
                    defaults={
                        'name': instance.category.name,
                        'account_type': AccountType.EXPENSE,
                        'description': f'Expenses for {instance.category.name}'
                    }
                )
                
                # Get or create cash/bank account
                asset_account, _ = Account.objects.get_or_create(
                    business=business,
                    code='1000',
                    defaults={
                        'name': 'Cash',
                        'account_type': AccountType.ASSET,
                        'description': 'Cash on hand'
                    }
                )
                
                # Create the transaction
                transaction_obj = Transaction.objects.create(
                    business=business,
                    date=instance.date,
                    description=f"Expense: {instance.category.name}",
                    reference=f"Expense-{instance.pk}"
                )
                
                # Create debit entry (increase in expense)
                TransactionEntry.objects.create(
                    transaction=transaction_obj,
                    account=expense_account,
                    business=business,
                    amount=instance.amount,
                    is_debit=True,
                    description=f"Expense: {instance.description or instance.category.name}"
                )
                
                # Create credit entry (decrease in asset)
                TransactionEntry.objects.create(
                    transaction=transaction_obj,
                    account=asset_account,
                    business=business,
                    amount=instance.amount,
                    is_debit=False,
                    description=f"Payment for expense: {instance.description or instance.category.name}"
                )
                
        except Exception as e:
            logger.error(f"Error creating accounting entries for expense {instance.pk}: {str(e)}")