from .middleware import get_current_business

def current_business(request):
    """
    Context processor to make the current business available in templates.
    """
    return {
        'current_business': get_current_business()
    }