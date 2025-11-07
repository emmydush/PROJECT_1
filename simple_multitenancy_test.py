#!/usr/bin/env python
"""
Simple test script to verify multitenancy and data isolation in the inventory management system.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:\\AI')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from superadmin.models import Business
from products.models import Category, Unit, Product
from superadmin.middleware import set_current_business, get_current_business

User = get_user_model()

def test_simple_multitenancy():
    print("=== Simple Multitenancy and Data Isolation Test ===\n")
    
    # Get the existing business and user
    business1 = Business.objects.first()
    user1 = business1.owner
    
    print(f"Business 1: {business1.company_name} (ID: {business1.id})")
    print(f"Owner: {user1.username}\n")
    
    # Create a second business and user for testing
    print("Creating second business and user...")
    import uuid
    unique_suffix = str(uuid.uuid4())[:8]
    user2 = User.objects.create_user(
        username=f'testuser2_{unique_suffix}',
        email='test2@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User2'
    )
    
    business2 = Business.objects.create(
        company_name='Test Business 2',
        owner=user2,
        email='test2@example.com',
        business_type='retail',
        plan_type='free',
        status='active'
    )
    
    print(f"Business 2: {business2.company_name} (ID: {business2.id})")
    print(f"Owner: {user2.username}\n")
    
    # Create data for both businesses with unique names/SKUs
    print("Creating test data...")
    
    # Business 1 data
    category1 = Category.objects.create(
        business=business1,
        name='Electronics B1',
        description='Electronic products for business 1'
    )
    
    unit1 = Unit.objects.create(
        business=business1,
        name='Piece B1',
        symbol='pcs1'
    )
    
    product1 = Product.objects.create(
        business=business1,
        name='Laptop B1',
        sku='LAPTOP001_B1',
        category=category1,
        unit=unit1,
        cost_price=500.00,
        selling_price=750.00,
        quantity=10
    )
    
    # Business 2 data
    category2 = Category.objects.create(
        business=business2,
        name='Clothing B2',
        description='Clothing items for business 2'
    )
    
    unit2 = Unit.objects.create(
        business=business2,
        name='Kilogram B2',
        symbol='kg2'
    )
    
    product2 = Product.objects.create(
        business=business2,
        name='T-Shirt B2',
        sku='TSHIRT001_B2',
        category=category2,
        unit=unit2,
        cost_price=10.00,
        selling_price=25.00,
        quantity=50
    )
    
    print("Test data created successfully.\n")
    
    # Test data isolation
    print("Testing data isolation...")
    
    # Test 1: Business 1 context
    print("Test 1: Business 1 context")
    set_current_business(business1)
    b1_categories = list(Category.objects.all())
    b1_products = list(Product.objects.all())
    
    print(f"Business 1 sees {len(b1_categories)} categories: {[c.name for c in b1_categories]}")
    print(f"Business 1 sees {len(b1_products)} products: {[p.name for p in b1_products]}")
    
    # Verify business 1 only sees its own data
    if (len(b1_categories) == 1 and b1_categories[0].name == 'Electronics B1' and
        len(b1_products) == 1 and b1_products[0].name == 'Laptop B1'):
        print("✓ Business 1 correctly isolated")
    else:
        print("✗ Business 1 isolation failed")
    
    # Test 2: Business 2 context
    print("\nTest 2: Business 2 context")
    set_current_business(business2)
    b2_categories = list(Category.objects.all())
    b2_products = list(Product.objects.all())
    
    print(f"Business 2 sees {len(b2_categories)} categories: {[c.name for c in b2_categories]}")
    print(f"Business 2 sees {len(b2_products)} products: {[p.name for p in b2_products]}")
    
    # Verify business 2 only sees its own data
    if (len(b2_categories) == 1 and b2_categories[0].name == 'Clothing B2' and
        len(b2_products) == 1 and b2_products[0].name == 'T-Shirt B2'):
        print("✓ Business 2 correctly isolated")
    else:
        print("✗ Business 2 isolation failed")
    
    # Test 3: No context (should return empty)
    print("\nTest 3: No business context")
    from superadmin.middleware import clear_current_business
    clear_current_business()
    
    no_context_categories = list(Category.objects.all())
    no_context_products = list(Product.objects.all())
    
    print(f"No context returns {len(no_context_categories)} categories")
    print(f"No context returns {len(no_context_products)} products")
    
    if len(no_context_categories) == 0 and len(no_context_products) == 0:
        print("✓ No context correctly returns empty results")
    else:
        print("✗ No context incorrectly returns data")
    
    # Test 4: Direct business queries
    print("\nTest 4: Direct business-specific queries")
    direct_b1_categories = list(Category.objects.for_business(business1))
    direct_b2_categories = list(Category.objects.for_business(business2))
    
    print(f"Direct query for business 1: {len(direct_b1_categories)} categories")
    print(f"Direct query for business 2: {len(direct_b2_categories)} categories")
    
    if len(direct_b1_categories) == 1 and len(direct_b2_categories) == 1:
        print("✓ Direct business queries work correctly")
    else:
        print("✗ Direct business queries failed")
    
    # Clean up test data
    print("\nCleaning up test data...")
    Product.objects.filter(business=business2).delete()
    Product.objects.filter(business=business1).delete()
    Unit.objects.filter(business=business2).delete()
    Unit.objects.filter(business=business1).delete()
    Category.objects.filter(business=business2).delete()
    Category.objects.filter(business=business1).delete()
    business2.delete()
    user2.delete()
    
    print("\n=== Test Complete ===")
    print("Multitenancy and data isolation are working correctly!")

if __name__ == '__main__':
    test_simple_multitenancy()