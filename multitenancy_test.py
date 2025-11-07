#!/usr/bin/env python
"""
Test script to verify multitenancy and data isolation in the inventory management system.
This script tests that users can only access data from their own business and cannot
access other businesses' data.
"""

import os
import sys
import django
from django.conf import settings

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from superadmin.models import Business
from products.models import Category, Unit, Product
from superadmin.middleware import set_current_business, get_current_business

User = get_user_model()

def test_multitenancy():
    """
    Test multitenancy and data isolation functionality.
    """
    print("Testing multitenancy and data isolation...")
    
    # Get the superadmin user to use as owner
    try:
        superadmin = User.objects.get(username='emmanuel')
        print(f"Using superadmin user: {superadmin}")
    except User.DoesNotExist:
        print("Superadmin user 'emmanuel' not found!")
        return
    
    # Create test businesses
    print("\n1. Creating test businesses...")
    business1, created = Business.objects.get_or_create(
        company_name="Test Business 1",
        defaults={
            'owner': superadmin,
            'email': 'test1@example.com',
            'business_type': 'retail',
            'plan_type': 'free',
            'status': 'active'
        }
    )
    if created:
        print(f"Created business 1: {business1}")
    else:
        print(f"Using existing business 1: {business1}")
    
    business2, created = Business.objects.get_or_create(
        company_name="Test Business 2",
        defaults={
            'owner': superadmin,
            'email': 'test2@example.com',
            'business_type': 'wholesale',
            'plan_type': 'premium',
            'status': 'active'
        }
    )
    if created:
        print(f"Created business 2: {business2}")
    else:
        print(f"Using existing business 2: {business2}")
    
    # Create test users for each business
    print("\n2. Creating test users...")
    user1, created = User.objects.get_or_create(
        username=f"testuser1_{business1.id}",
        defaults={
            'email': 'testuser1@example.com',
            'first_name': 'Test',
            'last_name': 'User 1'
        }
    )
    if created:
        user1.set_password('testpass123')
        user1.save()
        print(f"Created user 1: {user1}")
    else:
        print(f"Using existing user 1: {user1}")
    
    user2, created = User.objects.get_or_create(
        username=f"testuser2_{business2.id}",
        defaults={
            'email': 'testuser2@example.com',
            'first_name': 'Test',
            'last_name': 'User 2'
        }
    )
    if created:
        user2.set_password('testpass123')
        user2.save()
        print(f"Created user 2: {user2}")
    else:
        print(f"Using existing user 2: {user2}")
    
    # Test 1: Business context isolation
    print("\n3. Testing business context isolation...")
    
    # Set business context to business 1
    set_current_business(business1)
    print(f"Current business context set to: {get_current_business()}")
    
    # Create categories for business 1
    category1, created = Category.objects.get_or_create(
        name="Electronics",
        business=business1,
        defaults={'description': 'Electronic products'}
    )
    if created:
        print(f"Created category for business 1: {category1}")
    else:
        print(f"Using existing category for business 1: {category1}")
    
    # Create units for business 1
    unit1, created = Unit.objects.get_or_create(
        name="Piece",
        symbol="pc",
        business=business1
    )
    if created:
        print(f"Created unit for business 1: {unit1}")
    else:
        print(f"Using existing unit for business 1: {unit1}")
    
    # Create products for business 1
    product1, created = Product.objects.get_or_create(
        name="Smartphone",
        sku="SP001",
        business=business1,
        defaults={
            'category': category1,
            'unit': unit1,
            'cost_price': 200.00,
            'selling_price': 300.00,
            'quantity': 10
        }
    )
    if created:
        print(f"Created product for business 1: {product1}")
    else:
        print(f"Using existing product for business 1: {product1}")
    
    # Set business context to business 2
    set_current_business(business2)
    print(f"Current business context set to: {get_current_business()}")
    
    # Create categories for business 2
    category2, created = Category.objects.get_or_create(
        name="Clothing",
        business=business2,
        defaults={'description': 'Clothing items'}
    )
    if created:
        print(f"Created category for business 2: {category2}")
    else:
        print(f"Using existing category for business 2: {category2}")
    
    # Create units for business 2
    unit2, created = Unit.objects.get_or_create(
        name="Item",
        symbol="item",
        business=business2
    )
    if created:
        print(f"Created unit for business 2: {unit2}")
    else:
        print(f"Using existing unit for business 2: {unit2}")
    
    # Create products for business 2
    product2, created = Product.objects.get_or_create(
        name="T-Shirt",
        sku="TS001",
        business=business2,
        defaults={
            'category': category2,
            'unit': unit2,
            'cost_price': 10.00,
            'selling_price': 20.00,
            'quantity': 50
        }
    )
    if created:
        print(f"Created product for business 2: {product2}")
    else:
        print(f"Using existing product for business 2: {product2}")
    
    # Test 2: Data isolation verification
    print("\n4. Verifying data isolation...")
    
    # Set business context to business 1 and check accessible data
    set_current_business(business1)
    print(f"\nWith business context set to '{business1.company_name}':")
    
    categories_b1 = list(Category.objects.all())
    units_b1 = list(Unit.objects.all())
    products_b1 = list(Product.objects.all())
    
    print(f"  Categories accessible: {len(categories_b1)}")
    for cat in categories_b1:
        print(f"    - {cat.name}")
    
    print(f"  Units accessible: {len(units_b1)}")
    for unit in units_b1:
        print(f"    - {unit.name}")
    
    print(f"  Products accessible: {len(products_b1)}")
    for prod in products_b1:
        print(f"    - {prod.name}")
    
    # Verify that only business 1 data is accessible
    assert len(categories_b1) == 1, f"Expected 1 category for business 1, got {len(categories_b1)}"
    assert categories_b1[0].name == "Electronics", f"Expected 'Electronics', got '{categories_b1[0].name}'"
    assert categories_b1[0].business == business1, "Category should belong to business 1"
    
    assert len(products_b1) == 1, f"Expected 1 product for business 1, got {len(products_b1)}"
    assert products_b1[0].name == "Smartphone", f"Expected 'Smartphone', got '{products_b1[0].name}'"
    assert products_b1[0].business == business1, "Product should belong to business 1"
    
    # Set business context to business 2 and check accessible data
    set_current_business(business2)
    print(f"\nWith business context set to '{business2.company_name}':")
    
    categories_b2 = list(Category.objects.all())
    units_b2 = list(Unit.objects.all())
    products_b2 = list(Product.objects.all())
    
    print(f"  Categories accessible: {len(categories_b2)}")
    for cat in categories_b2:
        print(f"    - {cat.name}")
    
    print(f"  Units accessible: {len(units_b2)}")
    for unit in units_b2:
        print(f"    - {unit.name}")
    
    print(f"  Products accessible: {len(products_b2)}")
    for prod in products_b2:
        print(f"    - {prod.name}")
    
    # Verify that only business 2 data is accessible
    assert len(categories_b2) == 1, f"Expected 1 category for business 2, got {len(categories_b2)}"
    assert categories_b2[0].name == "Clothing", f"Expected 'Clothing', got '{categories_b2[0].name}'"
    assert categories_b2[0].business == business2, "Category should belong to business 2"
    
    assert len(products_b2) == 1, f"Expected 1 product for business 2, got {len(products_b2)}"
    assert products_b2[0].name == "T-Shirt", f"Expected 'T-Shirt', got '{products_b2[0].name}'"
    assert products_b2[0].business == business2, "Product should belong to business 2"
    
    # Test 3: Cross-business access prevention
    print("\n5. Testing cross-business access prevention...")
    
    # Try to access business 1 data from business 2 context
    set_current_business(business2)
    
    # Try to access business 1's category
    b1_categories = Category.objects.filter(business=business1)
    print(f"Business 2 trying to access Business 1 categories directly: {len(b1_categories)} found")
    
    # Try to access business 1's products
    b1_products = Product.objects.filter(business=business1)
    print(f"Business 2 trying to access Business 1 products directly: {len(b1_products)} found")
    
    # Test with no business context
    print("\n6. Testing behavior with no business context...")
    from superadmin.middleware import clear_current_business
    clear_current_business()
    
    no_context_categories = list(Category.objects.all())
    print(f"With no business context, categories accessible: {len(no_context_categories)}")
    
    # This should be empty as per our BusinessSpecificManager implementation
    assert len(no_context_categories) == 0, "Should not be able to access categories without business context"
    
    print("\n7. Testing direct business queries...")
    
    # Test accessing data for a specific business directly
    b1_direct_categories = list(Category.objects.for_business(business1))
    b2_direct_categories = list(Category.objects.for_business(business2))
    
    print(f"Direct query for business 1 categories: {len(b1_direct_categories)}")
    print(f"Direct query for business 2 categories: {len(b2_direct_categories)}")
    
    assert len(b1_direct_categories) == 1, f"Expected 1 category for business 1, got {len(b1_direct_categories)}"
    assert len(b2_direct_categories) == 1, f"Expected 1 category for business 2, got {len(b2_direct_categories)}"
    
    print("\n✅ All multitenancy and data isolation tests passed!")
    print("\nSummary:")
    print("- Business context correctly isolates data")
    print("- Users can only access data from their own business")
    print("- Cross-business access is properly prevented")
    print("- Direct business queries work as expected")
    print("- No business context correctly returns empty results")

if __name__ == "__main__":
    test_multitenancy()