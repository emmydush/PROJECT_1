import os
import sys
import django
from django.test import RequestFactory

# Add the project directory to the Python path
sys.path.append('e:\\AI')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

# Setup Django
django.setup()

from superadmin.middleware import BusinessContextMiddleware
from superadmin.models import Business
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.models import Session

def test_business_context():
    # Create a request factory
    factory = RequestFactory()
    
    # Create a mock request
    request = factory.get('/')
    
    # Add session middleware
    session_middleware = SessionMiddleware(lambda r: None)
    session_middleware.process_request(request)
    
    # Get the actual session from the database
    session = Session.objects.first()
    if session:
        request.session = session.get_decoded()
        print(f"Session data: {request.session}")
        print(f"Current business ID in session: {request.session.get('current_business_id', 'Not set')}")
    
    # Add auth middleware
    auth_middleware = AuthenticationMiddleware(lambda r: None)
    auth_middleware.process_request(request)
    
    # Apply business context middleware
    middleware = BusinessContextMiddleware(lambda r: None)
    middleware(request)
    
    # Check if business context is set
    from superadmin.middleware import get_current_business
    current_business = get_current_business()
    print(f"Current business after middleware: {current_business}")
    
    if current_business:
        print(f"Business name: {current_business.company_name}")
        
        # Test business-specific manager
        from products.models import Unit
        units = Unit.objects.business_specific()
        print(f"Units for current business: {units.count()}")
        for unit in units:
            print(f"  - {unit.name} ({unit.symbol})")
    else:
        print("No business context set")

if __name__ == "__main__":
    test_business_context()