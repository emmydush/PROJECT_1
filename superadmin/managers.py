from django.db import models
from django.db.models.query import QuerySet
from .middleware import get_current_business


class BusinessSpecificQuerySet(QuerySet):
    """
    Custom QuerySet that automatically filters objects by business context.
    This ensures data isolation in a multi-tenant environment.
    """
    
    def business_specific(self):
        """
        Filter objects by the current business context.
        This method should be called to ensure data isolation.
        """
        current_business = get_current_business()
        if current_business:
            # Check if the model has a direct business field
            if hasattr(self.model, 'business'):
                return self.filter(business=current_business)
            # Check if the model has a sale field (like SaleItem)
            elif hasattr(self.model, 'sale'):
                return self.filter(sale__business=current_business)
            # Check if the model has a cart field (like CartItem)
            elif hasattr(self.model, 'cart'):
                return self.filter(cart__business=current_business)
            # For other related models, we might need to add more conditions here
            else:
                # Fallback to original behavior
                return self.filter(business=current_business)
        return self.none()
    
    def create(self, **kwargs):
        """
        Override create to automatically associate objects with the current business.
        """
        current_business = get_current_business()
        # Only add business parameter for models that have a direct business field
        # Models like CartItem get their business context from their related objects
        if (current_business and 'business' not in kwargs and 
            hasattr(self.model, 'business')):
            kwargs['business'] = current_business
        return super().create(**kwargs)


class BusinessSpecificManager(models.Manager):
    """
    Custom Manager that automatically filters objects by business context.
    This ensures data isolation in a multi-tenant environment.
    """
    
    def get_queryset(self):
        """
        Return a BusinessSpecificQuerySet instance.
        """
        return BusinessSpecificQuerySet(self.model, using=self._db)
    
    def business_specific(self):
        """
        Filter objects by the current business context.
        This method should be called to ensure data isolation.
        """
        current_business = get_current_business()
        if current_business:
            # Check if the model has a direct business field
            if hasattr(self.model, 'business'):
                return self.get_queryset().filter(business=current_business)
            # Check if the model has a sale field (like SaleItem)
            elif hasattr(self.model, 'sale'):
                return self.get_queryset().filter(sale__business=current_business)
            # Check if the model has a cart field (like CartItem)
            elif hasattr(self.model, 'cart'):
                return self.get_queryset().filter(cart__business=current_business)
            # For other related models, we might need to add more conditions here
            else:
                # Fallback to original behavior
                return self.get_queryset().filter(business=current_business)
        return self.get_queryset().none()
    
    def create(self, **kwargs):
        """
        Override create to automatically associate objects with the current business.
        """
        current_business = get_current_business()
        # Only add business parameter for models that have a direct business field
        # Models like CartItem get their business context from their related objects
        if (current_business and 'business' not in kwargs and 
            hasattr(self.model, 'business')):
            kwargs['business'] = current_business
        return super().create(**kwargs)