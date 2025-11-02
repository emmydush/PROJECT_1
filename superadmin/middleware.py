from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from .models import Business
import threading

# Thread-local storage for business context
_thread_locals = threading.local()

def get_current_business():
    """
    Get the current business from thread-local storage.
    This is used by the business-specific managers to filter queries.
    """
    return getattr(_thread_locals, 'current_business', None)

def set_current_business(business):
    """
    Set the current business in thread-local storage.
    This is used by the business-specific managers to filter queries.
    """
    _thread_locals.current_business = business

class BusinessContextMiddleware(MiddlewareMixin):
    """
    Middleware to ensure each user request is associated with a business context.
    This is crucial for multi-tenancy data isolation.
    """
    
    def process_request(self, request):
        # Skip middleware for admin and API URLs
        if request.path.startswith('/admin/') or request.path.startswith('/api/'):
            return None
            
        # Skip middleware for authentication URLs
        if request.path.startswith('/accounts/') or request.path.startswith('/authentication/'):
            return None
            
        # Skip middleware for superadmin URLs
        if request.path.startswith('/superadmin/'):
            return None
            
        # If user is not authenticated, let Django's authentication handle it
        if not request.user.is_authenticated:
            return None
            
        # For superusers, we might want to allow access to all businesses
        if request.user.is_superuser:
            # Check if a business is selected in the session
            if 'current_business_id' in request.session:
                try:
                    business = Business.objects.get(id=request.session['current_business_id'])
                    request.current_business = business
                    set_current_business(business)  # Set in thread-local storage
                except Business.DoesNotExist:
                    # If the business doesn't exist, remove it from session
                    if 'current_business_id' in request.session:
                        del request.session['current_business_id']
                    request.current_business = None
                    set_current_business(None)  # Clear thread-local storage
            else:
                request.current_business = None
                set_current_business(None)  # Clear thread-local storage
            return None
            
        # For regular users, check if they have an associated business
        # This would typically be handled by assigning users to businesses
        # For now, we'll assume users are associated with businesses through a relationship
        
        # Try to get business from session first
        if 'current_business_id' in request.session:
            try:
                business = Business.objects.get(id=request.session['current_business_id'])
                # Verify user has access to this business
                if self.user_has_access_to_business(request.user, business):
                    request.current_business = business
                    set_current_business(business)  # Set in thread-local storage
                    return None
                else:
                    # User doesn't have access, redirect to business selection
                    set_current_business(None)  # Clear thread-local storage
                    # Only redirect if not already on business selection page
                    if not request.path.startswith('/business-selection/'):
                        return redirect('superadmin:business_selection')
            except Business.DoesNotExist:
                # If the business doesn't exist, remove it from session
                if 'current_business_id' in request.session:
                    del request.session['current_business_id']
                set_current_business(None)  # Clear thread-local storage
                # Only redirect if not already on business selection page
                if not request.path.startswith('/business-selection/'):
                    return redirect('superadmin:business_selection')
        else:
            # No business in session, redirect to business selection
            # But only if the user is not already on the business selection page
            if not request.path.startswith('/business-selection/'):
                set_current_business(None)  # Clear thread-local storage
                return redirect('superadmin:business_selection')
            else:
                set_current_business(None)  # Clear thread-local storage
                
        return None
        
    def user_has_access_to_business(self, user, business):
        """
        Check if a user has access to a specific business.
        This could be implemented in various ways:
        1. Direct ownership (user is the business owner)
        2. Membership (user is a member of the business)
        3. Role-based access (user has specific roles in the business)
        """
        # For now, we'll check if the user is the owner of the business
        # In a more complex system, you might have a many-to-many relationship
        # between users and businesses with roles
        return business.owner == user