from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import (
    Business, SubscriptionPlan, Subscription, Payment, SystemSetting,
    SystemLog, SecurityEvent, Announcement, SupportTicket, APIClient, APIRequestLog
)

User = get_user_model()

# Business & User Management
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'owner', 'email', 'plan_type', 'status', 'user_count', 'created_at')
    list_filter = ('plan_type', 'status', 'created_at')
    search_fields = ('company_name', 'owner__username', 'email')
    readonly_fields = ('created_at', 'updated_at')

# Note: User model is already registered in authentication app, so we don't register it here

# Subscription & Billing
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'max_products', 'max_users', 'max_branches', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('business', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan', 'is_active', 'start_date', 'end_date')
    search_fields = ('business__company_name', 'plan__name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'payment_method', 'transaction_id', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'subscription__business__company_name')

# System Configuration
@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
    search_fields = ('key', 'description')

# Reports & Analytics
@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('level', 'message', 'user', 'timestamp')
    list_filter = ('level', 'timestamp')
    search_fields = ('message', 'user__username')
    readonly_fields = ('timestamp',)

# Security Management
@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'user', 'ip_address', 'timestamp', 'is_resolved')
    list_filter = ('event_type', 'is_resolved', 'timestamp')
    search_fields = ('user__username', 'ip_address', 'details')
    readonly_fields = ('timestamp',)

# Communication Center
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('business', 'subject', 'priority', 'status', 'assigned_to', 'created_at')
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('subject', 'description', 'business__company_name')
    readonly_fields = ('created_at', 'updated_at')

# Developer / API Section
@admin.register(APIClient)
class APIClientAdmin(admin.ModelAdmin):
    list_display = ('business', 'name', 'api_key', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'business__company_name')
    readonly_fields = ('api_key', 'created_at', 'updated_at')

@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):
    list_display = ('api_client', 'endpoint', 'method', 'status_code', 'response_time', 'timestamp')
    list_filter = ('method', 'status_code', 'timestamp')
    search_fields = ('endpoint', 'api_client__business__company_name')
    readonly_fields = ('timestamp',)