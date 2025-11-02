from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, ExpenseCategory
from .forms import ExpenseForm, ExpenseCategoryForm
from superadmin.middleware import get_current_business

@login_required
def expense_list(request):
    expenses = Expense.objects.business_specific().all()
    return render(request, 'expenses/list.html', {'expenses': expenses})

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            # Get current business from middleware
            current_business = get_current_business()
            if current_business:
                # Save the expense with business context
                expense = form.save(commit=False)
                expense.business = current_business
                expense.save()
                messages.success(request, 'Expense created successfully!')
                return redirect('expenses:list')
            else:
                messages.error(request, 'No business context found. Please select a business.')
    else:
        form = ExpenseForm()
    
    return render(request, 'expenses/form.html', {'form': form, 'title': 'Create Expense'})

@login_required
def expense_detail(request, pk):
    expense = get_object_or_404(Expense.objects.business_specific(), pk=pk)
    return render(request, 'expenses/detail.html', {'expense': expense})

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense.objects.business_specific(), pk=pk)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expenses:detail', pk=expense.pk)
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'expenses/form.html', {
        'form': form, 
        'title': 'Update Expense',
        'expense': expense
    })

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense.objects.business_specific(), pk=pk)
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expenses:list')
    
    return render(request, 'expenses/confirm_delete.html', {'expense': expense})

@login_required
def category_list(request):
    categories = ExpenseCategory.objects.business_specific().all()
    return render(request, 'expenses/categories/list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            # Get current business from middleware
            current_business = get_current_business()
            if current_business:
                # Save the category with business context
                category = form.save(commit=False)
                category.business = current_business
                category.save()
                messages.success(request, 'Expense category created successfully!')
                return redirect('expenses:category_list')
            else:
                messages.error(request, 'No business context found. Please select a business.')
    else:
        form = ExpenseCategoryForm()
    
    return render(request, 'expenses/categories/form.html', {'form': form, 'title': 'Create Expense Category'})