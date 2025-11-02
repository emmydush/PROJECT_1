from django import template
from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def safe_provider_login_url(context, provider_id):
    """
    Safely generate a provider login URL, handling cases where the social app
    is not properly configured.
    """
    try:
        # Get the request from context
        request = context['request']
        
        # Check if the social app exists and is properly configured
        social_app = SocialApp.objects.filter(provider=provider_id).first()
        if not social_app or not social_app.client_id or not social_app.secret:
            # Return a placeholder URL that shows an alert
            return f"javascript:alert('Social authentication for {provider_id.title()} is not properly configured. Please contact the administrator.');"
        
        # Check if the social app is associated with the current site
        current_site = request.site if hasattr(request, 'site') else None
        if current_site and not social_app.sites.filter(id=current_site.id).exists():
            # Return a placeholder URL that shows an alert
            return f"javascript:alert('Social authentication for {provider_id.title()} is not properly configured for this site.');"
        
        # If everything is properly configured, generate the real URL
        provider = providers.registry.by_id(provider_id, request)
        return provider.get_login_url(request)
    except Exception:
        # If any error occurs, return a safe fallback
        return f"javascript:alert('Social authentication for {provider_id.title()} is not available at the moment.');"