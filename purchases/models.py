from django.db import models
from products.models import Product
from suppliers.models import Supplier
from superadmin.models import Business
from superadmin.managers import BusinessSpecificManager

class PurchaseOrder(models.Model):
    # Use business-specific manager
    objects = BusinessSpecificManager()
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('partially_received', 'Partially Received'),
        ('cancelled', 'Cancelled'),
    )
    
    # Add business relationship for multi-tenancy
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='purchase_orders', null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"PO-{self.pk} - {self.supplier.name}"

class PurchaseItem(models.Model):
    # Use business-specific manager
    objects = BusinessSpecificManager()
    
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    received_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    @property
    def is_fully_received(self):
        return self.received_quantity >= self.quantity

    @property
    def pending_quantity(self):
        return self.quantity - self.received_quantity