import os
import django
import json

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.db import transaction
from authentication.models import User
from superadmin.models import Business
from products.models import Product
from sales.models import Sale, SaleItem

def test_direct_sale():
    print("Testing direct sale creation...")
    
    # Get a user
    try:
        user = User.objects.get(username='stockmanager')
        print(f"Found user: {user.username}")
    except User.DoesNotExist:
        print("User not found")
        return
    
    # Get a business
    try:
        business = Business.objects.get(owner=user)
        print(f"Found business: {business.company_name}")
    except Business.DoesNotExist:
        print("Business not found")
        return
    
    # Get a product
    try:
        product = Product.objects.first()
        print(f"Found product: {product.name}")
    except Product.DoesNotExist:
        print("Product not found")
        return
    
    # Create a sale directly
    try:
        with transaction.atomic():
            sale = Sale.objects.create(
                business=business,
                subtotal=product.selling_price,
                total_amount=product.selling_price,
                payment_method='cash'
            )
            print(f"Sale created: {sale.id}")
            
            # Create a sale item
            sale_item = SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=1,
                unit_price=product.selling_price,
                total_price=product.selling_price
            )
            print(f"Sale item created: {sale_item.id}")
            
        print("Direct sale creation successful!")
        return True
    except Exception as e:
        print(f"Error creating direct sale: {e}")
        return False

if __name__ == '__main__':
    test_direct_sale()