"""
Test script to verify branch management functionality
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from superadmin.models import Business, Branch

User = get_user_model()

def test_branch_management():
    # Create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        email='test@example.com',
        defaults={'first_name': 'Test', 'last_name': 'User'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print("Created test user")
    
    # Create a test business
    business, created = Business.objects.get_or_create(
        company_name='Test Business',
        email='business@test.com',
        owner=user,
        defaults={'business_type': 'retail', 'plan_type': 'free', 'status': 'active'}
    )
    if created:
        print("Created test business")
    
    # Create test branches
    branch1, created = Branch.objects.get_or_create(
        business=business,
        name='Main Branch',
        address='123 Main St, City, Country',
        phone='+1234567890',
        email='main@test.com',
        defaults={'is_main': True, 'is_active': True}
    )
    if created:
        print("Created main branch")
    
    branch2, created = Branch.objects.get_or_create(
        business=business,
        name='Secondary Branch',
        address='456 Secondary St, City, Country',
        phone='+0987654321',
        email='secondary@test.com',
        defaults={'is_main': False, 'is_active': True}
    )
    if created:
        print("Created secondary branch")
    
    # Assign manager to branch2
    branch2.manager = user
    branch2.save()
    print(f"Assigned {user.username} as manager of {branch2.name}")
    
    # List all branches for the business
    branches = Branch.objects.filter(business=business)
    print(f"\nBranches for {business.company_name}:")
    for branch in branches:
        status = "Active" if branch.is_active else "Inactive"
        main = " (Main)" if branch.is_main else ""
        manager = f" (Manager: {branch.manager.username})" if branch.manager else " (No manager)"
        print(f"- {branch.name}{main} - {status}{manager}")
        print(f"  Address: {branch.address}")
        print(f"  Contact: {branch.phone}, {branch.email}")
    
    print("\nTest completed successfully!")

if __name__ == '__main__':
    test_branch_management()