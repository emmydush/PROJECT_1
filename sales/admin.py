from django.contrib import admin
from .models import Sale, SaleItem, Refund

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = ('total_price', 'created_at')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'sale_date', 'subtotal', 'tax', 'discount', 'total_amount', 'payment_method', 'is_refunded')
    list_filter = ('payment_method', 'is_refunded', 'sale_date')
    search_fields = ('id', 'customer__first_name', 'customer__last_name', 'customer__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SaleItemInline]
    date_hierarchy = 'sale_date'
    ordering = ('-sale_date',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('customer', 'notes')
        }),
        ('Financial Details', {
            'fields': ('subtotal', 'tax', 'discount', 'total_amount', 'payment_method')
        }),
        ('Status', {
            'fields': ('is_refunded',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'unit_price', 'total_price', 'created_at')
    list_filter = ('sale', 'product', 'created_at')
    search_fields = ('sale__id', 'product__name')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('sale', 'reason', 'refund_amount', 'refund_date')
    list_filter = ('refund_date',)
    search_fields = ('sale__id', 'reason')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-refund_date',)