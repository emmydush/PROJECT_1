import os
import django
import json

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from authentication.models import User
from superadmin.models import Business
from sales.cart_views import add_to_cart, get_or_create_cart
from products.models import Product

def dummy_get_response(request):
    return None

def test_cart_functionality():
    print("Testing cart functionality...")
    
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
    
    # Get a product directly
    try:
        product = Product.objects.first()
        print(f"Found product: {product.name}")
    except Product.DoesNotExist:
        print("Product not found")
        return
    
    # Create a request
    request = factory.post('/sales/cart/add/', 
                          data=json.dumps({
                              'product_id': product.id,
                              'quantity': 1
                          }),
                          content_type='application/json')
    
    # Add user to request
    request.user = user
    
    # Add session to request
    middleware = SessionMiddleware(dummy_get_response)
    middleware.process_request(request)
    request.session.save()
    
    # Set business in session
    request.session['current_business_id'] = business.id
    print(f"Set business ID in session: {business.id}")
    
    # Test get_or_create_cart
    try:
        cart = get_or_create_cart(request)
        print(f"Cart created/retrieved: {cart.id}")
    except Exception as e:
        print(f"Error getting/creating cart: {e}")
        return
    
    # Test add_to_cart
    try:
        response = add_to_cart(request)
        print(f"Add to cart response status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content)
            print(f"Add to cart success: {data}")
        else:
            print(f"Add to cart failed: {response.content}")
    except Exception as e:
        print(f"Error in add_to_cart: {e}")

if __name__ == '__main__':
    test_cart_functionality()