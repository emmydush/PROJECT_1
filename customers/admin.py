from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'company', 'loyalty_points', 'credit_limit', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'company')
    ordering = ('first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address')
        }),
        ('Business Information', {
            'fields': ('company',)
        }),
        ('Loyalty & Credit', {
            'fields': ('loyalty_points', 'credit_limit')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )