from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from superadmin.middleware import get_current_business
from products.models import Unit

@login_required
def test_business_context(request):
    # Get current business from middleware
    current_business = get_current_business()
    
    # Get units using business-specific manager
    units = Unit.objects.business_specific()
    
    # Get all units for comparison
    all_units = Unit.objects.all()
    
    response_data = {
        'current_business': current_business.company_name if current_business else None,
        'current_business_id': current_business.id if current_business else None,
        'business_specific_units_count': units.count(),
        'all_units_count': all_units.count(),
        'session_business_id': request.session.get('current_business_id'),
        'units': [{'name': u.name, 'symbol': u.symbol} for u in units]
    }
    
    return JsonResponse(response_data)