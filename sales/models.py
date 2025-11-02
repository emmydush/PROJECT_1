from django.db import models
from django.conf import settings
from products.models import Product
from customers.models import Customer
from decimal import Decimal
from superadmin.models import Business
from superadmin.managers import BusinessSpecificManager

class Sale(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
    )
    
    # Use business-specific manager
    objects = BusinessSpecificManager()
    
    # Add business relationship for multi-tenancy
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='sales', null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    sale_date = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    notes = models.TextField(blank=True, null=True)
    is_refunded = models.BooleanField(default=False)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-sale_date']

    def __str__(self):
        return f"Sale-{self.pk}"

    @property
    def total_profit(self):
        """Calculate total profit for this sale"""
        profit = Decimal('0')
        for item in self.items.all():
            profit += item.total_profit
        return profit

class SaleItem(models.Model):
    # Use business-specific manager
    objects = BusinessSpecificManager()
    
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.total_price = Decimal(str(self.quantity)) * Decimal(str(self.unit_price))
        super().save(*args, **kwargs)

    @property
    def cost_price(self):
        """Get the cost price of the product at the time of sale"""
        return self.product.cost_price

    @property
    def profit_per_unit(self):
        """Calculate profit per unit for this sale item"""
        return Decimal(str(self.unit_price)) - Decimal(str(self.cost_price))

    @property
    def total_profit(self):
        """Calculate total profit for this sale item"""
        return self.profit_per_unit * Decimal(str(self.quantity))

# New Cart model for the improved POS system
class Cart(models.Model):
    # Use business-specific manager
    objects = BusinessSpecificManager()
    
    # Add business relationship for multi-tenancy
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='carts', null=True)
    session_key = models.CharField(max_length=40, unique=True)  # For anonymous users
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # For logged-in users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart {self.session_key}"

class CartItem(models.Model):
    # Use business-specific manager
    objects = BusinessSpecificManager()
    
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of adding to cart
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('cart', 'product')  # One product per cart
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return Decimal(str(self.quantity)) * Decimal(str(self.unit_price))
    
    def save(self, *args, **kwargs):
        # Set unit price from product if not already set
        if not self.unit_price:
            self.unit_price = self.product.selling_price
        super().save(*args, **kwargs)

class Refund(models.Model):
    # Use business-specific manager
    objects = BusinessSpecificManager()
    
    # Add business relationship for multi-tenancy
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='refunds', null=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    reason = models.TextField()
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Refund for Sale-{self.sale.pk}"