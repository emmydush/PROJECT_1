from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product, Category, Unit
from sales.models import Sale, SaleItem
from purchases.models import PurchaseOrder, PurchaseItem

class StockAutomationTest(TestCase):
    def setUp(self):
        # Create a user
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create category and unit
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category for testing'
        )
        
        self.unit = Unit.objects.create(
            name='Pieces',
            symbol='pcs'
        )
        
        # Create a product
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST001',
            category=self.category,
            unit=self.unit,
            cost_price=10.00,
            selling_price=15.00,
            quantity=100,
            reorder_level=10
        )
        
        # Create a customer for sales
        from customers.models import Customer
        self.customer = Customer.objects.create(
            first_name='Test',
            last_name='Customer',
            email='customer@example.com',
            phone='1234567890',
            is_active=True
        )
        
        # Create a supplier for purchases
        from suppliers.models import Supplier
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='supplier@example.com',
            phone='0987654321',
            is_active=True
        )

    def test_stock_reduction_on_sale(self):
        """Test that product stock is reduced when a sale is made"""
        initial_quantity = self.product.quantity
        
        # Create a sale
        sale = Sale.objects.create(
            customer=self.customer,
            subtotal=30.00,
            total_amount=30.00,
            payment_method='cash'
        )
        
        # Create sale items
        sale_item = SaleItem.objects.create(
            sale=sale,
            product=self.product,
            quantity=5,
            unit_price=15.00,
            total_price=75.00
        )
        
        # Refresh product from database
        self.product.refresh_from_db()
        
        # Check that stock was reduced
        self.assertEqual(float(self.product.quantity), float(initial_quantity) - 5)

    def test_stock_increase_on_purchase_receive(self):
        """Test that product stock is increased when purchase items are received"""
        initial_quantity = self.product.quantity
        
        # Create a purchase order
        purchase_order = PurchaseOrder.objects.create(
            supplier=self.supplier,
            total_amount=100.00,
            status='pending'
        )
        
        # Create purchase items
        purchase_item = PurchaseItem.objects.create(
            purchase_order=purchase_order,
            product=self.product,
            quantity=20,
            unit_price=10.00,
            total_price=200.00,
            received_quantity=0
        )
        
        # Increment the received quantity to simulate receiving items (like in the view)
        purchase_item.received_quantity += 10
        purchase_item.save()
        
        # Refresh product from database
        self.product.refresh_from_db()
        
        # Check that stock was increased
        self.assertEqual(float(self.product.quantity), float(initial_quantity) + 10)

    def test_stock_restoration_on_sale_delete(self):
        """Test that product stock is restored when a sale item is deleted"""
        initial_quantity = self.product.quantity
        
        # Create a sale
        sale = Sale.objects.create(
            customer=self.customer,
            subtotal=30.00,
            total_amount=30.00,
            payment_method='cash'
        )
        
        # Create sale items
        sale_item = SaleItem.objects.create(
            sale=sale,
            product=self.product,
            quantity=5,
            unit_price=15.00,
            total_price=75.00
        )
        
        # Refresh product from database
        self.product.refresh_from_db()
        quantity_after_sale = self.product.quantity
        
        # Delete the sale item
        sale_item.delete()
        
        # Refresh product from database
        self.product.refresh_from_db()
        
        # Check that stock was restored
        self.assertEqual(float(self.product.quantity), float(initial_quantity))