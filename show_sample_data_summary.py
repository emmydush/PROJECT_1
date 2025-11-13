from superadmin.models import Business
from products.models import Product
from customers.models import Customer
from suppliers.models import Supplier
from products.models import Category, Unit
from superadmin.middleware import set_current_business

def show_summary():
    print('Sample Data Summary:')
    print('==================')
    businesses = Business.objects.all()
    for business in businesses:
        set_current_business(business)
        print(f'{business.company_name}:')
        print(f'  Products: {Product.objects.count()}')
        print(f'  Customers: {Customer.objects.count()}')
        print(f'  Suppliers: {Supplier.objects.count()}')
        print(f'  Categories: {Category.objects.count()}')
        print(f'  Units: {Unit.objects.count()}')
        print()

if __name__ == '__main__':
    show_summary()