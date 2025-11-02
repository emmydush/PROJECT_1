from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Supplier
from .forms import SupplierForm
from superadmin.middleware import get_current_business

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.business_specific().filter(is_active=True)
    return render(request, 'suppliers/list.html', {'suppliers': suppliers})

@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            # Get the current business from middleware
            current_business = get_current_business()
            if current_business:
                # Save the supplier with the business context
                supplier = form.save(commit=False)
                supplier.business = current_business
                supplier.save()
                messages.success(request, 'Supplier created successfully!')
                return redirect('suppliers:list')
            else:
                messages.error(request, 'No business context found. Please select a business.')
    else:
        form = SupplierForm()
    
    return render(request, 'suppliers/form.html', {'form': form, 'title': 'Create Supplier'})

@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier.objects.business_specific(), pk=pk)
    return render(request, 'suppliers/detail.html', {'supplier': supplier})

@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier.objects.business_specific(), pk=pk)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully!')
            return redirect('suppliers:detail', pk=supplier.pk)
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'suppliers/form.html', {
        'form': form, 
        'title': 'Update Supplier',
        'supplier': supplier
    })

@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier.objects.business_specific(), pk=pk)
    
    if request.method == 'POST':
        supplier.is_active = False
        supplier.save()
        messages.success(request, 'Supplier deleted successfully!')
        return redirect('suppliers:list')
    
    return render(request, 'suppliers/confirm_delete.html', {'supplier': supplier})