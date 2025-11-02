import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from sales.views import pos_view
from django.test import RequestFactory
from authentication.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from superadmin.models import Business

def dummy_get_response(request):
    return None

def test_pos_view():
    print("Testing POS view...")
    
    # Create a request factory
    factory = RequestFactory()
    
    # Create a request
    request = factory.get('/sales/pos/')
    
    # Get a user
    try:
        user = User.objects.get(username='stockmanager')
        print(f"Found user: {user.username}")
        request.user = user
    except User.DoesNotExist:
        print("User not found")
        return
    
    # Add session to request
    middleware = SessionMiddleware(dummy_get_response)
    middleware.process_request(request)
    request.session.save()
    
    # Get a business
    try:
        business = Business.objects.get(owner=user)
        print(f"Found business: {business.company_name}")
        # Set business in session
        request.session['current_business_id'] = business.id
        print(f"Set business ID in session: {business.id}")
        
        # Set business context in thread-local storage
        from superadmin.middleware import set_current_business
        set_current_business(business)
        print("Set business context in thread-local storage")
    except Business.DoesNotExist:
        print("Business not found")
        return
    
    # Test POS view
    try:
        response = pos_view(request)
        print(f"POS view response status: {response.status_code}")
        if response.status_code == 200:
            print("POS view works correctly!")
        else:
            print(f"POS view failed with status: {response.status_code}")
    except Exception as e:
        print(f"Error in POS view: {e}")

if __name__ == '__main__':
    test_pos_view()