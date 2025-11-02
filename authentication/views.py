from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import User
from superadmin.models import Business
from superadmin.forms import BusinessDetailsForm

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Handle remember me functionality if needed
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                
                # Check if user has a business
                user_businesses = Business.objects.filter(owner=user)
                if not user_businesses.exists():
                    # Redirect to business details page
                    return redirect('authentication:business_details')
                else:
                    # Set the first business as the current business in session
                    first_business = user_businesses.first()
                    request.session['current_business_id'] = first_business.id
                    # Also set in middleware thread-local storage
                    from superadmin.middleware import set_current_business
                    set_current_business(first_business)
                    return redirect('dashboard:index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('authentication:login')

def register_view(request):
    """Simplified single-step registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('authentication:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'authentication/register_simple.html', {
        'form': form
    })

@login_required
def business_details_view(request):
    """View for new users to enter their business details after registration"""
    # Check if user already has a business
    existing_business = Business.objects.filter(owner=request.user)
    if existing_business.exists():
        # If user already has a business, redirect to dashboard
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = BusinessDetailsForm(request.POST)
        if form.is_valid():
            # Create the business
            business = form.save(commit=False)
            business.owner = request.user
            business.plan_type = 'free'
            business.status = 'active'
            business.save()
            
            # Set the business in session
            request.session['current_business_id'] = business.id
            
            # Also set in middleware thread-local storage
            from superadmin.middleware import set_current_business
            set_current_business(business)
            
            messages.success(request, 'Business details saved successfully!')
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusinessDetailsForm()
    
    return render(request, 'authentication/business_details.html', {'form': form})

def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('authentication:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'authentication/profile.html', {'form': form})

@login_required
def user_list_view(request):
    from .models import User
    users = User.objects.all()
    return render(request, 'authentication/user_list.html', {'users': users})

def password_reset_view(request):
    # For now, we'll just render a simple template
    # In a real application, you would implement password reset functionality
    return render(request, 'authentication/password_reset.html')