from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from sales.models import Sale
from customers.models import Customer
from purchases.models import PurchaseOrder
from expenses.models import Expense
from django.db.models import Sum, Count, F
from decimal import Decimal
from superadmin.models import Business
from superadmin.middleware import set_current_business  # Import the middleware function
import logging

# Set up logging
logger = logging.getLogger(__name__)

@login_required
def dashboard_view(request):
    logger.info("=== DASHBOARD VIEW START ===")
    logger.info(f"User: {request.user}")
    logger.info(f"Session: {dict(request.session)}")
    
    # Check if there's a current business in the session
    current_business = None
    if 'current_business_id' in request.session:
        try:
            current_business = Business.objects.get(id=request.session['current_business_id'])
            logger.info(f"Found business in session: {current_business}")
        except Business.DoesNotExist:
            # If the business doesn't exist, remove it from session
            logger.warning("Business not found in session, removing from session")
            del request.session['current_business_id']
            current_business = None
    else:
        logger.warning("No current_business_id in session")
    
    # If no business is selected, try to get the first business owned by the user
    if not current_business:
        user_businesses = Business.objects.filter(owner=request.user)
        logger.info(f"User businesses count: {user_businesses.count()}")
        if user_businesses.exists():
            current_business = user_businesses.first()
            logger.info(f"Using first business: {current_business}")
            # Set it in the session for future requests
            request.session['current_business_id'] = current_business.id
        else:
            logger.warning("No businesses found for user, redirecting to create business")
            # Check if user has just registered and needs to create a business
            # Redirect to business creation page
            return redirect('authentication:create_business')
    
    # IMPORTANT: Set the current business in middleware thread-local storage
    # This is required for business_specific() manager method to work properly
    if current_business:
        set_current_business(current_business)
        logger.info(f"Set current business in middleware: {current_business}")
    
    # Get business-specific data using business_specific() manager
    logger.info(f"Fetching business-specific data for business: {current_business}")
    products = Product.objects.business_specific()
    sales = Sale.objects.business_specific()
    customers = Customer.objects.business_specific()
    purchases = PurchaseOrder.objects.business_specific()
    expenses = Expense.objects.business_specific()
    
    logger.info(f"Products count: {products.count()}")
    logger.info(f"Sales count: {sales.count()}")
    logger.info(f"Customers count: {customers.count()}")
    logger.info(f"Purchases count: {purchases.count()}")
    logger.info(f"Expenses count: {expenses.count()}")
    
    # Calculate dashboard statistics
    total_products = products.count()
    total_sales = sales.count()
    total_customers = customers.count()
    total_purchases = purchases.count()
    
    # Calculate today's sales
    from django.utils import timezone
    today = timezone.now().date()
    today_sales_queryset = sales.filter(sale_date__date=today)
    today_sales = today_sales_queryset.count()
    logger.info(f"Today's sales count: {today_sales}")
    
    # Calculate low stock products
    low_stock_products = products.filter(quantity__lte=F('reorder_level'))
    low_stock_count = low_stock_products.count()
    logger.info(f"Low stock products count: {low_stock_count}")
    
    # Calculate out of stock products
    out_of_stock_count = products.filter(quantity=0).count()
    logger.info(f"Out of stock products count: {out_of_stock_count}")
    
    # Calculate today's profit
    today_profit = Decimal('0.00')
    today_sales_objects = today_sales_queryset
    for sale in today_sales_objects:
        today_profit += sale.total_profit
        logger.info(f"Sale {sale.id} profit: {sale.total_profit}")
    
    logger.info(f"Today's total profit: {today_profit}")
    
    context = {
        'total_products': total_products,
        'total_sales': total_sales,
        'total_customers': total_customers,
        'total_purchases': total_purchases,
        'today_sales': today_sales,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'today_profit': today_profit,
        'low_stock_products': low_stock_products[:5],  # Limit to 5 for display
        'current_business': current_business,
    }
    
    logger.info(f"Context data: {context}")
    logger.info("=== DASHBOARD VIEW END ===")
    
    return render(request, 'dashboard.html', context)