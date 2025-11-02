from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'contact_person', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'phone', 'company', 'contact_person')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'company', 'tax_id')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Contact Person', {
            'fields': ('contact_person', 'contact_person_phone', 'contact_person_email')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )