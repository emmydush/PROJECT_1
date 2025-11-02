import os
import django
import json
import uuid

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from authentication.models import User
from superadmin.models import Business
from products.models import Product
from sales.models import Cart, CartItem
from sales.cart_views import process_sale_from_cart

def dummy_get_response(request):
    return None

def test_cart_direct():
    print("Testing cart functionality directly...")
    
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
    
    # Create a unique session key (max 40 characters)
    session_key = f'test_{uuid.uuid4().hex[:35]}'
    print(f"Using session key: {session_key}")
    
    # Create or get a cart for testing
    try:
        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            business=business,
            defaults={'user': user}
        )
        if created:
            print(f"Created new cart: {cart.id}")
        else:
            print(f"Found existing cart: {cart.id}")
            # Clear existing items
            cart.items.all().delete()
    except Exception as e:
        print(f"Error creating/getting cart: {e}")
        return
    
    # Add item to cart directly
    try:
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=2,
            unit_price=product.selling_price
        )
        print(f"Added item to cart: {cart_item.id}")
    except Exception as e:
        print(f"Error adding item to cart: {e}")
        return
    
    # Verify cart has items
    try:
        cart_items = cart.items.all()
        print(f"Cart has {cart_items.count()} items")
        for item in cart_items:
            print(f"  - {item.product.name}: {item.quantity} x {item.unit_price} = {item.total_price}")
    except Exception as e:
        print(f"Error getting cart items: {e}")
        return
    
    # Test processing sale from cart
    print("\n--- Test: Processing sale from cart ---")
    
    # Create a request factory
    factory = RequestFactory()
    
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
    
    # Manually set business context in thread-local storage
    from superadmin.middleware import set_current_business
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
            if data.get('success'):
                print("Sale processing completed successfully!")
                return True
        else:
            print(f"Process sale failed: {response.content}")
            # Try to decode the content
            try:
                error_data = json.loads(response.content)
                print(f"Error details: {error_data}")
            except:
                print(f"Raw error content: {response.content}")
    except Exception as e:
        print(f"Error in process_sale_from_cart: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == '__main__':
    test_cart_direct()