from django.contrib import admin
from .models import PurchaseOrder, PurchaseItem

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    readonly_fields = ('total_price', 'created_at')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'order_date', 'expected_delivery_date', 'status', 'total_amount')
    list_filter = ('status', 'order_date', 'expected_delivery_date')
    search_fields = ('id', 'supplier__name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PurchaseItemInline]
    date_hierarchy = 'order_date'
    ordering = ('-order_date',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('supplier', 'expected_delivery_date', 'notes')
        }),
        ('Financial Details', {
            'fields': ('total_amount',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase_order', 'product', 'quantity', 'received_quantity', 'unit_price', 'total_price', 'is_fully_received')
    list_filter = ('purchase_order', 'product')
    search_fields = ('purchase_order__id', 'product__name')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def is_fully_received(self, obj):
        return obj.is_fully_received
    is_fully_received.boolean = True
    is_fully_received.short_description = 'Fully Received'