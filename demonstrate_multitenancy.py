#!/usr/bin/env python
"""
Simple demonstration script for multitenancy and data isolation.
This script shows how the multi-tenancy system works in practice.
"""

import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from superadmin.models import Business
from products.models import Category, Unit, Product
from superadmin.middleware import set_current_business, get_current_business, clear_current_business

User = get_user_model()

def demonstrate_multitenancy():
    """
    Demonstrate how multitenancy works in the system.
    """
    print("=== Multitenancy Demonstration ===\n")
    
    # Get the superadmin user
    superadmin = User.objects.get(username='emmanuel')
    
    # Create two test businesses
    print("1. Creating two test businesses...")
    business1, _ = Business.objects.get_or_create(
        company_name="Demo Business 1",
        defaults={
            'owner': superadmin,
            'email': 'demo1@example.com',
            'business_type': 'retail',
            'plan_type': 'free',
            'status': 'active'
        }
    )
    print(f"   Business 1: {business1.company_name}")
    
    business2, _ = Business.objects.get_or_create(
        company_name="Demo Business 2",
        defaults={
            'owner': superadmin,
            'email': 'demo2@example.com',
            'business_type': 'wholesale',
            'plan_type': 'premium',
            'status': 'active'
        }
    )
    print(f"   Business 2: {business2.company_name}\n")
    
    # Create data for Business 1
    print("2. Creating data for Business 1...")
    set_current_business(business1)
    
    # Create a category for Business 1
    electronics_cat, _ = Category.objects.get_or_create(
        name="Electronics",
        business=business1,
        defaults={'description': 'Electronic products'}
    )
    print(f"   Created category: {electronics_cat.name}")
    
    # Create a unit for Business 1
    piece_unit, _ = Unit.objects.get_or_create(
        name="Piece",
        symbol="pc",
        business=business1
    )
    print(f"   Created unit: {piece_unit.name}")
    
    # Create a product for Business 1
    smartphone, _ = Product.objects.get_or_create(
        name="Smartphone",
        sku="SP001",
        business=business1,
        defaults={
            'category': electronics_cat,
            'unit': piece_unit,
            'cost_price': 200.00,
            'selling_price': 300.00,
            'quantity': 10
        }
    )
    print(f"   Created product: {smartphone.name}\n")
    
    # Create data for Business 2
    print("3. Creating data for Business 2...")
    set_current_business(business2)
    
    # Create a category for Business 2
    clothing_cat, _ = Category.objects.get_or_create(
        name="Clothing",
        business=business2,
        defaults={'description': 'Clothing items'}
    )
    print(f"   Created category: {clothing_cat.name}")
    
    # Create a unit for Business 2
    item_unit, _ = Unit.objects.get_or_create(
        name="Item",
        symbol="item",
        business=business2
    )
    print(f"   Created unit: {item_unit.name}")
    
    # Create a product for Business 2
    tshirt, _ = Product.objects.get_or_create(
        name="T-Shirt",
        sku="TS001",
        business=business2,
        defaults={
            'category': clothing_cat,
            'unit': item_unit,
            'cost_price': 10.00,
            'selling_price': 20.00,
            'quantity': 50
        }
    )
    print(f"   Created product: {tshirt.name}\n")
    
    # Demonstrate data isolation
    print("4. Demonstrating data isolation...")
    
    # View data as Business 1
    set_current_business(business1)
    print(f"   Viewing data as {business1.company_name}:")
    print(f"     Current categories: {[c.name for c in Category.objects.all()]}")
    print(f"     Current products: {[p.name for p in Product.objects.all()]}\n")
    
    # View data as Business 2
    set_current_business(business2)
    print(f"   Viewing data as {business2.company_name}:")
    print(f"     Current categories: {[c.name for c in Category.objects.all()]}")
    print(f"     Current products: {[p.name for p in Product.objects.all()]}\n")
    
    # Demonstrate direct business queries
    print("5. Demonstrating direct business queries...")
    clear_current_business()  # Clear current context
    
    print("   With no business context:")
    print(f"     Categories accessible: {Category.objects.count()}")
    print(f"     Products accessible: {Product.objects.count()}\n")
    
    print("   Using direct business queries:")
    b1_categories = Category.objects.for_business(business1)
    b2_categories = Category.objects.for_business(business2)
    print(f"     Business 1 categories: {[c.name for c in b1_categories]}")
    print(f"     Business 2 categories: {[c.name for c in b2_categories]}\n")
    
    # Clean up
    print("6. Cleaning up demo data...")
    Business.objects.filter(company_name__startswith="Demo Business").delete()
    print("   Demo data cleaned up.\n")
    
    print("✅ Multitenancy demonstration completed successfully!")
    print("\nKey Points:")
    print("- Each business sees only its own data")
    print("- No business context means no data access")
    print("- Direct queries can access specific business data")
    print("- Data isolation is automatic and secure")

if __name__ == "__main__":
    demonstrate_multitenancy()