import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

# Now we can import Django models
from sales.models import Cart, CartItem, Sale, SaleItem
from products.models import Product
from superadmin.models import Business
from superadmin.middleware import set_current_business
from authentication.models import User
from customers.models import Customer

def test_sale_processing():
    try:
        # Create a test user
        user = User.objects.first()
        if not user:
            print("No user found in database")
            return
            
        # Get a business
        business = Business.objects.first()
        if not business:
            print("No business found in database")
            return
            
        # Set the current business context
        set_current_business(business)
        print(f"Set current business to: {business}")
            
        # Create a cart for the user
        cart = Cart.objects.create(
            user=user,
            business=business,
            session_key="test_session"
        )
        print(f"Created cart: {cart}")
        
        # Get a product
        product = Product.objects.filter(business=business, name__startswith='Script Test Product').first()
        if not product:
            print("No product found in database")
            return
            
        print(f"Using product: {product.name}")
        
        # Add item to cart
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1,
            unit_price=product.selling_price,
            business=business
        )
        print(f"Created cart item: {cart_item}")
        
        # Create a sale
        sale = Sale.objects.create(
            subtotal=product.selling_price,
            tax=0,
            discount=0,
            total_amount=product.selling_price,
            payment_method='cash',
            business=business
        )
        print(f"Created sale: {sale}")
        
        # Create sale item
        sale_item = SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=1,
            unit_price=product.selling_price,
            total_price=product.selling_price,
            business=business
        )
        print(f"Created sale item: {sale_item}")
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sale_processing()