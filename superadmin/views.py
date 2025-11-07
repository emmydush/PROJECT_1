from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.db.models import Count, Sum, Avg, Max, Min
from django.utils import timezone
from datetime import timedelta, datetime
from .models import (
    Business, Branch, SubscriptionPlan, Subscription, Payment, SystemSetting,
    SystemLog, SecurityEvent, Announcement, SupportTicket, APIClient, APIRequestLog
)
from authentication.models import User
from products.models import Product
from sales.models import Sale
from customers.models import Customer
from purchases.models import PurchaseOrder
from expenses.models import Expense
from .middleware import set_current_business
from .forms import BranchForm, BusinessDetailsForm
import psutil
import platform
import csv

def is_superadmin(user):
    return user.is_superuser and user.is_staff

@method_decorator([user_passes_test(is_superadmin)], name='dispatch')
class SuperAdminDashboardView(TemplateView):
    template_name = 'superadmin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Business & User Management stats
        context['total_businesses'] = Business.objects.count()
        context['active_businesses'] = Business.objects.filter(status='active').count()
        context['pending_businesses'] = Business.objects.filter(status='pending').count()
        context['suspended_businesses'] = Business.objects.filter(status='suspended').count()
        context['total_users'] = User.objects.count()
        
        # Subscription & Billing stats
        context['total_subscriptions'] = Subscription.objects.count()
        context['active_subscriptions'] = Subscription.objects.filter(is_active=True).count()
        context['total_revenue'] = Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # System stats
        context['total_logs'] = SystemLog.objects.count()
        context['security_events'] = SecurityEvent.objects.filter(is_resolved=False).count()
        context['open_tickets'] = SupportTicket.objects.filter(status='open').count()
        
        # Recent activities
        context['recent_businesses'] = Business.objects.order_by('-created_at')[:5]
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        context['recent_logs'] = SystemLog.objects.order_by('-timestamp')[:10]
        
        # Security monitoring
        context['recent_security_events'] = SecurityEvent.objects.order_by('-timestamp')[:10]
        context['unresolved_security_events'] = SecurityEvent.objects.filter(is_resolved=False).count()
        context['suspended_users'] = User.objects.filter(is_active=False).count()
        
        # API monitoring
        context['api_clients'] = APIClient.objects.count()
        context['active_api_clients'] = APIClient.objects.filter(is_active=True).count()
        
        # Enhanced analytics for owner dashboard
        # Total active users across all tenants
        context['total_active_users'] = User.objects.filter(is_active=True).count()
        
        # Business distribution by plan type
        context['business_plan_distribution'] = Business.objects.values('plan_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Monthly system usage (simplified - using API request logs)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        context['monthly_usage'] = APIRequestLog.objects.filter(
            timestamp__gte=thirty_days_ago
        ).count()
        
        # Revenue by plan type
        context['revenue_by_plan'] = Subscription.objects.filter(
            is_active=True
        ).values('plan__name').annotate(
            total_revenue=Sum('plan__price')
        )
        
        # Business activity metrics
        context['business_metrics'] = {
            'total_products': Product.objects.count(),
            'total_sales': Sale.objects.count(),
            'total_sales_value': Sale.objects.aggregate(
                total=Sum('total_amount')
            )['total'] or 0,
        }
        
        # Subscription status distribution
        context['subscription_status_distribution'] = Subscription.objects.values('is_active').annotate(
            count=Count('id')
        )
        
        return context

@method_decorator([user_passes_test(is_superadmin)], name='dispatch')
class BusinessManagementView(TemplateView):
    template_name = 'superadmin/business_management.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all businesses with related data
        businesses = Business.objects.all().prefetch_related('subscriptions', 'branches', 'users')
        
        # Enhance businesses with additional information
        business_data = []
        for business in businesses:
            # Get subscription info
            subscription = business.subscriptions.first()
            subscription_status = "No Subscription"
            if subscription:
                if subscription.is_active:
                    if subscription.end_date > timezone.now():
                        subscription_status = "Active"
                    else:
                        subscription_status = "Expired"
                else:
                    subscription_status = "Inactive"
            elif business.created_at > timezone.now() - timedelta(days=14):
                subscription_status = "Trial"
            
            # Get branch count
            branch_count = business.branches.count()
            
            # Get user count
            user_count = business.users.count()
            
            # Get last activity (simplified - using last login of owner)
            last_activity = business.owner.last_login or business.owner.date_joined
            
            business_data.append({
                'business': business,
                'subscription_status': subscription_status,
                'branch_count': branch_count,
                'user_count': user_count,
                'last_activity': last_activity,
            })
        
        context['businesses'] = business_data
        context['users'] = User.objects.all()
        context['total_businesses'] = Business.objects.count()
        context['active_businesses'] = Business.objects.filter(status='active').count()
        context['suspended_businesses'] = Business.objects.filter(status='suspended').count()
        
        # Add recent tenant activity logs (simplified using system logs)
        context['tenant_logs'] = SystemLog.objects.order_by('-timestamp')[:20]
        return context

@method_decorator([user_passes_test(is_superadmin)], name='dispatch')
class SubscriptionManagementView(TemplateView):
    template_name = 'superadmin/subscription_management.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = SubscriptionPlan.objects.all()
        context['subscriptions'] = Subscription.objects.all()
        context['payments'] = Payment.objects.all()
        return context

@method_decorator([user_passes_test(is_superadmin)], name='dispatch')
class SystemLogsView(TemplateView):
    template_name = 'superadmin/system_logs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all system logs
        context['logs'] = SystemLog.objects.select_related('user', 'business').order_by('-timestamp')[:100]
        
        # Get security events
        context['security_events'] = SecurityEvent.objects.select_related('user', 'business').order_by('-timestamp')[:100]
        
        # Get login history
        context['login_events'] = SecurityEvent.objects.select_related('user').filter(
            event_type='login_attempt'
        ).order_by('-timestamp')[:50]
        
        # Get suspicious activities
        context['suspicious_activities'] = SecurityEvent.objects.select_related('user', 'business').filter(
            event_type__in=['suspicious_activity', 'account_lockout', 'failed_logins', 'data_export']
        ).order_by('-timestamp')[:50]
        
        # Stats
        context['total_logs'] = SystemLog.objects.count()
        context['total_security_events'] = SecurityEvent.objects.count()
        context['total_login_attempts'] = SecurityEvent.objects.filter(
            event_type='login_attempt'
        ).count()
        
        return context


class UserActivityLogsView(TemplateView):
    template_name = 'superadmin/user_activity_logs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current business from middleware
        from superadmin.middleware import get_current_business
        current_business = get_current_business()
        
        if current_business:
            # Get all users for this business
            business_users = User.objects.filter(businesses=current_business)
            
            # Get system logs for users in this business
            context['logs'] = SystemLog.objects.filter(
                user__in=business_users
            ).select_related('user').order_by('-timestamp')[:100]
            
            # Get security events for users in this business
            context['security_events'] = SecurityEvent.objects.filter(
                user__in=business_users
            ).select_related('user').order_by('-timestamp')[:100]
            
            # Get login history for users in this business
            context['login_events'] = SecurityEvent.objects.filter(
                user__in=business_users,
                event_type='login_attempt'
            ).select_related('user').order_by('-timestamp')[:50]
            
            # Get suspicious activities for users in this business
            context['suspicious_activities'] = SecurityEvent.objects.filter(
                user__in=business_users,
                event_type__in=['suspicious_activity', 'account_lockout', 'failed_logins', 'data_export']
            ).select_related('user').order_by('-timestamp')[:50]
            
            # Stats for this business
            context['total_logs'] = SystemLog.objects.filter(user__in=business_users).count()
            context['total_security_events'] = SecurityEvent.objects.filter(user__in=business_users).count()
            context['total_login_attempts'] = SecurityEvent.objects.filter(
                user__in=business_users,
                event_type='login_attempt'
            ).count()
        else:
            # If no business context, show empty results
            context['logs'] = SystemLog.objects.none()
            context['security_events'] = SecurityEvent.objects.none()
            context['login_events'] = SecurityEvent.objects.none()
            context['suspicious_activities'] = SecurityEvent.objects.none()
            context['total_logs'] = 0
            context['total_security_events'] = 0
            context['total_login_attempts'] = 0
        
        return context

@method_decorator([user_passes_test(is_superadmin)], name='dispatch')
class CommunicationCenterView(TemplateView):
    template_name = 'superadmin/communication_center.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all announcements
        context['announcements'] = Announcement.objects.all()
        
        # Get all support tickets
        context['tickets'] = SupportTicket.objects.select_related('business', 'assigned_to').all().order_by('-created_at')
        
        # Get ticket statistics
        context['ticket_stats'] = {
            'open': SupportTicket.objects.filter(status='open').count(),
            'in_progress': SupportTicket.objects.filter(status='in_progress').count(),
            'resolved': SupportTicket.objects.filter(status='resolved').count(),
            'closed': SupportTicket.objects.filter(status='closed').count(),
        }
        
        # Get recent feedback (simulated with support tickets)
        context['recent_feedback'] = SupportTicket.objects.filter(
            priority='low'
        ).order_by('-created_at')[:10]
        
        return context

@method_decorator([user_passes_test(is_superadmin)], name='dispatch')
class APIMonitoringView(TemplateView):
    template_name = 'superadmin/api_monitoring.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # API clients
        context['api_clients'] = APIClient.objects.all()
        
        # API request logs
        context['api_logs'] = APIRequestLog.objects.order_by('-timestamp')[:50]
        
        # API usage statistics
        context['total_api_requests'] = APIRequestLog.objects.count()
        context['api_requests_today'] = APIRequestLog.objects.filter(
            timestamp__date=timezone.now().date()
        ).count()
        
        # API clients statistics
        context['active_api_clients'] = APIClient.objects.filter(is_active=True).count()
        context['total_api_clients'] = APIClient.objects.count()
        
        # API performance metrics
        context['avg_response_time'] = APIRequestLog.objects.aggregate(
            avg_time=Avg('response_time')
        )['avg_time'] or 0
        
        # API endpoint usage
        context['endpoint_usage'] = APIRequestLog.objects.values('endpoint').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # API status codes distribution
        context['status_code_distribution'] = APIRequestLog.objects.values('status_code').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return context

@method_decorator([user_passes_test(is_superadmin)], name='dispatch')
class SystemMonitoringView(TemplateView):
    template_name = 'superadmin/system_monitoring.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # System information
        try:
            context['cpu_percent'] = psutil.cpu_percent(interval=1)
            context['memory_info'] = psutil.virtual_memory()
            context['disk_usage'] = psutil.disk_usage('/')
            context['boot_time'] = psutil.boot_time()
            context['uptime'] = timezone.now().timestamp() - context['boot_time']
            
            # Format uptime
            uptime_seconds = int(context['uptime'])
            days = uptime_seconds // (24 * 3600)
            uptime_seconds = uptime_seconds % (24 * 3600)
            hours = uptime_seconds // 3600
            uptime_seconds %= 3600
            minutes = uptime_seconds // 60
            
            context['uptime_formatted'] = f"{days} days, {hours} hours, {minutes} minutes"
            
            # System info
            context['system_info'] = {
                'platform': platform.system(),
                'platform_version': platform.version(),
                'architecture': platform.architecture()[0],
                'processor': platform.processor(),
                'python_version': platform.python_version(),
            }
        except Exception as e:
            # If psutil is not available or fails, provide fallback data
            context['cpu_percent'] = 0
            context['memory_info'] = None
            context['disk_usage'] = None
            context['uptime_formatted'] = "Unknown"
            context['system_info'] = {
                'platform': "Unknown",
                'platform_version': "Unknown",
                'architecture': "Unknown",
                'processor': "Unknown",
                'python_version': platform.python_version(),
            }
        
        # Error logs
        context['error_logs'] = SystemLog.objects.filter(level='error').order_by('-timestamp')[:20]
        context['critical_logs'] = SystemLog.objects.filter(level='critical').order_by('-timestamp')[:10]
        
        # Failed transactions (simulated with sales marked as refunded)
        context['failed_transactions'] = Sale.objects.filter(is_refunded=True).order_by('-updated_at')[:10]
        
        # Notifications
        context['recent_notifications'] = SystemLog.objects.filter(
            level__in=['warning', 'error', 'critical']
        ).order_by('-timestamp')[:15]
        
        # API monitoring summary
        context['api_summary'] = {
            'total_requests': APIRequestLog.objects.count(),
            'requests_today': APIRequestLog.objects.filter(
                timestamp__date=timezone.now().date()
            ).count(),
            'avg_response_time': APIRequestLog.objects.aggregate(
                avg_time=Avg('response_time')
            )['avg_time'] or 0,
        }
        
        return context

# Financial Dashboard View
@method_decorator([user_passes_test(is_superadmin)], name='dispatch')
class FinancialDashboardView(TemplateView):
    template_name = 'superadmin/financial_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current date and calculate date ranges
        today = timezone.now().date()
        first_day_current_month = today.replace(day=1)
        first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)
        last_day_last_month = first_day_current_month - timedelta(days=1)
        
        # Total revenue
        context['total_revenue'] = Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Revenue this month
        context['revenue_this_month'] = Payment.objects.filter(
            status='completed',
            created_at__date__gte=first_day_current_month
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Revenue last month
        context['revenue_last_month'] = Payment.objects.filter(
            status='completed',
            created_at__date__gte=first_day_last_month,
            created_at__date__lte=last_day_last_month
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Calculate profit change
        if context['revenue_last_month'] > 0:
            context['profit_change_percentage'] = (
                (context['revenue_this_month'] - context['revenue_last_month']) / 
                context['revenue_last_month']
            ) * 100
        else:
            context['profit_change_percentage'] = 100 if context['revenue_this_month'] > 0 else 0
        
        # Upcoming payments (subscriptions ending in next 30 days)
        next_30_days = timezone.now() + timedelta(days=30)
        context['upcoming_payments'] = Subscription.objects.filter(
            is_active=True,
            end_date__lte=next_30_days,
            end_date__gte=timezone.now()
        ).order_by('end_date')[:10]
        
        # Revenue per tenant
        business_revenue = []
        businesses = Business.objects.all().prefetch_related('subscriptions')
        for business in businesses:
            # Get payments for this business's subscriptions
            business_subscriptions = business.subscriptions.all()
            subscription_ids = business_subscriptions.values_list('id', flat=True)
            business_payments = Payment.objects.filter(
                subscription_id__in=subscription_ids,
                status='completed'
            )
            
            total_revenue = business_payments.aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            business_revenue.append({
                'business': business,
                'total_revenue': total_revenue,
                'subscription_count': business_subscriptions.count(),
            })
        
        context['business_revenue'] = business_revenue
        
        # Subscription plan revenue distribution
        context['plan_revenue_distribution'] = SubscriptionPlan.objects.annotate(
            total_revenue=Sum(
                'subscription__payment__amount',
                filter=models.Q(subscription__payment__status='completed')
            )
        ).order_by('-total_revenue')
        
        # Recent payments
        context['recent_payments'] = Payment.objects.select_related(
            'subscription__business', 'subscription__plan'
        ).order_by('-created_at')[:10]
        
        return context

# User Management View
@method_decorator([user_passes_test(is_superadmin)], name='dispatch')
class UserManagementView(TemplateView):
    template_name = 'superadmin/user_management.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all users with their business information
        users = User.objects.all().prefetch_related('businesses')
        
        # Enhance users with additional information
        user_data = []
        for user in users:
            # Get businesses associated with the user
            businesses = user.businesses.all()
            
            # Get last login
            last_login = user.last_login or user.date_joined
            
            user_data.append({
                'user': user,
                'businesses': businesses,
                'last_login': last_login,
                'business_count': businesses.count(),
            })
        
        context['users'] = user_data
        context['total_users'] = User.objects.count()
        context['active_users'] = User.objects.filter(is_active=True).count()
        context['suspended_users'] = User.objects.filter(is_active=False).count()
        
        # Get role distribution with percentage
        total_users_count = context['total_users']
        role_distribution = User.objects.values('role').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Add percentage to each role
        role_distribution_with_percentage = []
        for role_data in role_distribution:
            percentage = round((role_data['count'] / total_users_count) * 100, 1) if total_users_count > 0 else 0
            role_data['percentage'] = percentage
            role_distribution_with_percentage.append(role_data)
        
        context['role_distribution'] = role_distribution_with_percentage
        
        return context

# Export financial reports
@user_passes_test(is_superadmin)
def export_financial_report(request):
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="financial_report.csv"'
    
    writer = csv.writer(response)
    
    # Write header
    writer.writerow([
        'Business Name', 
        'Subscription Plan', 
        'Payment Amount', 
        'Payment Status', 
        'Payment Date',
        'Transaction ID'
    ])
    
    # Write data
    payments = Payment.objects.select_related(
        'subscription__business', 
        'subscription__plan'
    ).order_by('-created_at')
    
    for payment in payments:
        writer.writerow([
            payment.subscription.business.company_name,
            payment.subscription.plan.name,
            payment.amount,
            payment.status,
            payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            payment.transaction_id
        ])
    
    return response

# Business selection view for regular users
def business_selection_view(request):
    """
    View to allow users to select which business they want to work with.
    This is crucial for multi-tenancy data isolation.
    """
    # Get businesses that the user has access to
    # For now, we'll assume users can access businesses they own
    # In a more complex system, you might have a many-to-many relationship
    # between users and businesses with roles
    user_businesses = Business.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        business_id = request.POST.get('business_id')
        if business_id:
            try:
                business = Business.objects.get(id=business_id, owner=request.user)
                # Store the selected business in the session
                request.session['current_business_id'] = business.id
                # Also set in middleware thread-local storage
                set_current_business(business)
                # Redirect to the dashboard
                return redirect('dashboard:index')
            except Business.DoesNotExist:
                messages.error(request, 'Invalid business selection.')
        else:
            messages.error(request, 'Please select a business.')
    
    context = {
        'businesses': user_businesses
    }
    return render(request, 'superadmin/business_selection.html', context)

# Add branch management views here
@login_required
def branch_list_view(request):
    """View to list all branches for the current business"""
    from superadmin.middleware import get_current_business
    current_business = get_current_business()
    
    if not current_business:
        messages.error(request, 'No business context found.')
        return redirect('dashboard:index')
    
    branches = Branch.objects.filter(business=current_business)
    
    return render(request, 'superadmin/branch_list.html', {
        'branches': branches,
        'business': current_business
    })

@login_required
def branch_create_view(request):
    """View to create a new branch for the current business"""
    from superadmin.middleware import get_current_business
    current_business = get_current_business()
    
    if not current_business:
        messages.error(request, 'No business context found.')
        return redirect('dashboard:index')
    
    # Check if user has permission to create branches (only admins)
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to create branches.')
        return redirect('superadmin:branch_list')
    
    if request.method == 'POST':
        form = BranchForm(request.POST, business=current_business)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.business = current_business
            
            # If this is the first branch, make it the main branch
            if not Branch.objects.filter(business=current_business).exists():
                branch.is_main = True
            
            branch.save()
            
            # If this branch is marked as main, unset other branches
            if branch.is_main:
                Branch.objects.filter(
                    business=current_business, 
                    is_main=True
                ).exclude(id=branch.id).update(is_main=False)
            
            messages.success(request, f'Branch "{branch.name}" created successfully!')
            return redirect('superadmin:branch_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BranchForm(business=current_business)
    
    return render(request, 'superadmin/branch_form.html', {
        'form': form,
        'business': current_business,
        'title': 'Create Branch'
    })

@login_required
def branch_update_view(request, branch_id):
    """View to update an existing branch"""
    from superadmin.middleware import get_current_business
    current_business = get_current_business()
    
    if not current_business:
        messages.error(request, 'No business context found.')
        return redirect('dashboard:index')
    
    # Check if user has permission to edit branches (only admins)
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to edit branches.')
        return redirect('superadmin:branch_list')
    
    branch = get_object_or_404(Branch, id=branch_id, business=current_business)
    
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch, business=current_business)
        if form.is_valid():
            branch = form.save()
            
            # If this branch is marked as main, unset other branches
            if branch.is_main:
                Branch.objects.filter(
                    business=current_business, 
                    is_main=True
                ).exclude(id=branch.id).update(is_main=False)
            
            messages.success(request, f'Branch "{branch.name}" updated successfully!')
            return redirect('superadmin:branch_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BranchForm(instance=branch, business=current_business)
    
    return render(request, 'superadmin/branch_form.html', {
        'form': form,
        'business': current_business,
        'branch': branch,
        'title': 'Update Branch'
    })

@login_required
def branch_delete_view(request, branch_id):
    """View to delete a branch"""
    from superadmin.middleware import get_current_business
    current_business = get_current_business()
    
    if not current_business:
        messages.error(request, 'No business context found.')
        return redirect('dashboard:index')
    
    # Check if user has permission to delete branches (only admins)
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to delete branches.')
        return redirect('superadmin:branch_list')
    
    branch = get_object_or_404(Branch, id=branch_id, business=current_business)
    
    if request.method == 'POST':
        branch_name = branch.name
        branch.delete()
        messages.success(request, f'Branch "{branch_name}" deleted successfully!')
        return redirect('superadmin:branch_list')
    
    return render(request, 'superadmin/branch_confirm_delete.html', {
        'branch': branch,
        'business': current_business
    })

@login_required
def business_update_view(request):
    """View to update business details"""
    from superadmin.middleware import get_current_business
    current_business = get_current_business()
    
    if not current_business:
        messages.error(request, 'No business context found.')
        return redirect('dashboard:index')
    
    # Check if user has permission to update business details (only admins)
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to update business details.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = BusinessDetailsForm(request.POST, instance=current_business)
        if form.is_valid():
            business = form.save()
            messages.success(request, 'Business details updated successfully!')
            return redirect('superadmin:business_update')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusinessDetailsForm(instance=current_business)
    
    return render(request, 'superadmin/business_form.html', {
        'form': form,
        'business': current_business,
        'title': 'Update Business Details'
    })

@login_required
def business_deactivate_view(request):
    """View to deactivate the current business"""
    from superadmin.middleware import get_current_business
    current_business = get_current_business()
    
    if not current_business:
        messages.error(request, 'No business context found.')
        return redirect('dashboard:index')
    
    # Check if user has permission to deactivate business (only owner)
    if request.user != current_business.owner:
        messages.error(request, 'Only the business owner can deactivate the business.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        current_business.status = 'suspended'
        current_business.save()
        messages.success(request, 'Business has been deactivated successfully!')
        return redirect('dashboard:index')
    
    return render(request, 'superadmin/business_confirm_deactivate.html', {
        'business': current_business
    })

@login_required
def switch_branch_view(request, branch_id):
    """View to switch the current branch context"""
    from superadmin.middleware import get_current_business
    current_business = get_current_business()
    
    if not current_business:
        messages.error(request, 'No business context found.')
        return redirect('dashboard:index')
    
    # Check if the branch belongs to the current business
    try:
        branch = Branch.objects.get(id=branch_id, business=current_business)
        # Store the selected branch in the session
        request.session['current_branch_id'] = branch.id
        messages.success(request, f'Switched to branch: {branch.name}')
    except Branch.DoesNotExist:
        messages.error(request, 'Invalid branch selection.')
    
    # Redirect back to the dashboard
    return redirect('dashboard:index')

@login_required
def branch_reports_view(request):
    """View to generate combined reports from all branches"""
    from superadmin.middleware import get_current_business
    current_business = get_current_business()
    
    if not current_business:
        messages.error(request, 'No business context found.')
        return redirect('dashboard:index')
    
    # Check if user has permission to view reports (only admins and managers)
    if request.user.role not in ['admin', 'manager']:
        messages.error(request, 'You do not have permission to view branch reports.')
        return redirect('dashboard:index')
    
    # Get all branches for the current business
    branches = Branch.objects.filter(business=current_business, is_active=True)
    
    # Calculate branch-specific metrics
    # NOTE: Since branch fields were removed from models, we can't filter data by branch
    # We'll show overall business metrics for each branch (same data for all branches)
    branch_metrics = []
    for branch in branches:
        # Get business-specific data (no branch filtering available)
        branch_products = Product.objects.business_specific()
        branch_sales = Sale.objects.business_specific()
        branch_customers = Customer.objects.business_specific()
        branch_purchases = PurchaseOrder.objects.business_specific()
        branch_expenses = Expense.objects.business_specific()
        
        # Calculate metrics
        total_products = branch_products.count()
        total_sales = branch_sales.count()
        total_customers = branch_customers.count()
        total_purchases = branch_purchases.count()
        total_expenses = branch_expenses.count()
        
        # Calculate total sales value
        total_sales_value = branch_sales.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        # Calculate total expenses value
        total_expenses_value = branch_expenses.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        branch_metrics.append({
            'branch': branch,
            'total_products': total_products,
            'total_sales': total_sales,
            'total_customers': total_customers,
            'total_purchases': total_purchases,
            'total_expenses': total_expenses,
            'total_sales_value': total_sales_value,
            'total_expenses_value': total_expenses_value,
        })
    
    # Calculate overall business metrics
    overall_products = Product.objects.business_specific().count()
    overall_sales = Sale.objects.business_specific().count()
    overall_customers = Customer.objects.business_specific().count()
    overall_purchases = PurchaseOrder.objects.business_specific().count()
    overall_expenses = Expense.objects.business_specific().count()
    
    # Calculate overall sales value
    overall_sales_value = Sale.objects.business_specific().aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Calculate overall expenses value
    overall_expenses_value = Expense.objects.business_specific().aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    context = {
        'business': current_business,
        'branches': branches,
        'branch_metrics': branch_metrics,
        'overall_products': overall_products,
        'overall_sales': overall_sales,
        'overall_customers': overall_customers,
        'overall_purchases': overall_purchases,
        'overall_expenses': overall_expenses,
        'overall_sales_value': overall_sales_value,
        'overall_expenses_value': overall_expenses_value,
    }
    
    return render(request, 'superadmin/branch_reports.html', context)
