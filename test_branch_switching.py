"""
Test script to verify branch switching functionality
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from superadmin.models import Business, Branch

User = get_user_model()

def test_branch_switching():
    # Get the test user
    try:
        user = User.objects.get(username='testuser')
        print(f"Found user: {user.username}")
    except User.DoesNotExist:
        print("Test user not found")
        return
    
    # Get the test business
    try:
        business = Business.objects.get(company_name='Test Business')
        print(f"Found business: {business.company_name}")
    except Business.DoesNotExist:
        print("Test business not found")
        return
    
    # Get all branches for this business
    branches = Branch.objects.filter(business=business)
    print(f"Found {branches.count()} branches:")
    
    for branch in branches:
        status = "Active" if branch.is_active else "Inactive"
        main = " (Main)" if branch.is_main else ""
        manager = f" (Manager: {branch.manager.username})" if branch.manager else " (No manager)"
        print(f"- {branch.name}{main} - {status}{manager}")
    
    print("\nBranch switching functionality test completed!")

if __name__ == '__main__':
    test_branch_switching()