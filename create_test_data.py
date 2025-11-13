import os
import django
import uuid

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

# Now we can import Django models
from django.db import transaction
from superadmin.models import Business
from products.models import Category, Unit, Product

def create_test_data():
    try:
        business = Business.objects.first()
        print(f"Business: {business}")
        
        # Create category with unique name
        category_name = f"Script Test Category {uuid.uuid4().hex[:6]}"
        category = Category.objects.create(
            name=category_name,
            business=business
        )
        print(f"Created category: {category}")
        
        # Create unit with unique name and symbol
        unit_name = f"Script Test Unit {uuid.uuid4().hex[:6]}"
        symbol = f"stu_{uuid.uuid4().hex[:6]}"
        unit = Unit.objects.create(
            name=unit_name,
            symbol=symbol,
            business=business
        )
        print(f"Created unit: {unit}")
        
        # Create product with unique name and SKU
        product_name = f"Script Test Product {uuid.uuid4().hex[:6]}"
        sku = f"STP{uuid.uuid4().hex[:6]}"
        product = Product(
            name=product_name,
            sku=sku,
            category=category,
            unit=unit,
            cost_price=10.00,
            selling_price=15.00,
            business=business
        )
        product.save()
        print(f"Created product: {product}")
        print(f"Product ID: {product.id}")
        print(f"Product exists: {Product.objects.filter(id=product.id).exists()}")
        
        return product
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    create_test_data()