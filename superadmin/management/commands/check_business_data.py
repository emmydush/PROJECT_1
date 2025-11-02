from django.core.management.base import BaseCommand
from superadmin.models import Business
from products.models import Product
from sales.models import Sale
from customers.models import Customer
from purchases.models import PurchaseOrder
from expenses.models import Expense

class Command(BaseCommand):
    help = 'Check data for a specific business'

    def add_arguments(self, parser):
        parser.add_argument('business_id', type=int, help='ID of the business to check')

    def handle(self, *args, **options):
        try:
            business = Business.objects.get(id=options['business_id'])
            self.stdout.write(f'Business: {business.company_name}')
            self.stdout.write(f'Owner: {business.owner.username} ({business.owner.email})')
            self.stdout.write('=' * 50)
            
            # Count related data
            products_count = Product.objects.filter(business=business).count()
            sales_count = Sale.objects.filter(business=business).count()
            customers_count = Customer.objects.filter(business=business).count()
            purchases_count = PurchaseOrder.objects.filter(business=business).count()
            expenses_count = Expense.objects.filter(business=business).count()
            
            self.stdout.write(f'Products: {products_count}')
            self.stdout.write(f'Sales: {sales_count}')
            self.stdout.write(f'Customers: {customers_count}')
            self.stdout.write(f'Purchases: {purchases_count}')
            self.stdout.write(f'Expenses: {expenses_count}')
            
        except Business.DoesNotExist:
            self.stdout.write(f'Business with ID {options["business_id"]} does not exist.')