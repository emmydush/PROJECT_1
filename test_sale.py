import os
import django
import json

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from authentication.models import User
from superadmin.models import Business
from sales.cart_views import process_sale_from_cart, add_to_cart
from products.models import Product
from sales.models import Cart, CartItem

def dummy_get_response(request):
    return None

def test_sale_functionality():
    print("Testing sale functionality...")
    
    # Create a request factory
    factory = RequestFactory()
    
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
    
    # Create a request for adding to cart
    add_request = factory.post('/sales/cart/add/', 
                              data=json.dumps({
                                  'product_id': product.id,
                                  'quantity': 1
                              }),
                              content_type='application/json')
    
    # Add user to request
    add_request.user = user
    
    # Add session to request
    middleware = SessionMiddleware(dummy_get_response)
    middleware.process_request(add_request)
    add_request.session.save()
    
    # Set business in session
    add_request.session['current_business_id'] = business.id
    print(f"Set business ID in session: {business.id}")
    
    # Set business context in thread-local storage
    from superadmin.middleware import set_current_business
    set_current_business(business)
    print("Set business context in thread-local storage")
    
    # Test add_to_cart
    try:
        response = add_to_cart(add_request)
        print(f"Add to cart response status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content)
            print(f"Add to cart success: {data}")
        else:
            print(f"Add to cart failed: {response.content}")
            return
    except Exception as e:
        print(f"Error in add_to_cart: {e}")
        return
    
    # Create a request for processing sale
    sale_request = factory.post('/sales/cart/process/', 
                               data=json.dumps({
                                   'payment_method': 'cash',
                                   'discount': 0
                               }),
                               content_type='application/json')
    
    # Add user to request
    sale_request.user = user
    
    # Add session to request
    middleware = SessionMiddleware(dummy_get_response)
    middleware.process_request(sale_request)
    sale_request.session.save()
    
    # Set business in session
    sale_request.session['current_business_id'] = business.id
    print(f"Set business ID in session for sale: {business.id}")
    
    # Set business context in thread-local storage
    set_current_business(business)
    print("Set business context in thread-local storage for sale")
    
    # Add CSRF token to request
    sale_request.META['CSRF_COOKIE'] = 'test-csrf-token'
    
    # Test process_sale_from_cart
    try:
        response = process_sale_from_cart(sale_request)
        print(f"Process sale response status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content)
            print(f"Process sale success: {data}")
        else:
            print(f"Process sale failed: {response.content}")
    except Exception as e:
        print(f"Error in process_sale_from_cart: {e}")

if __name__ == '__main__':
    test_sale_functionality()