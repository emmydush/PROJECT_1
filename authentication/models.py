from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
        ('stock_manager', 'Stock Manager'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    businesses = models.ManyToManyField('superadmin.Business', related_name='users', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
    def has_custom_permission(self, permission_name):
        """
        Check if the user has a specific custom permission.
        First checks user-specific permissions, then role-based permissions.
        """
        from django.core.exceptions import ObjectDoesNotExist
        
        try:
            # Check if user has specific permission assigned
            user_perm = self.custom_permissions.get(permission__name=permission_name)
            return user_perm.granted
        except ObjectDoesNotExist:
            # If no user-specific permission, check role permissions
            try:
                role_perm = RolePermission.objects.get(
                    role=self.role,
                    permission__name=permission_name
                )
                return True
            except ObjectDoesNotExist:
                return False

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=50,
        help_text='Category for grouping permissions'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Permissions"

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.CharField(
        max_length=20,
        choices=User.ROLE_CHOICES
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Role Permissions"
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role} - {self.permission.name}"

class UserPermission(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='custom_permissions'
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE
    )
    granted = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Permissions"
        unique_together = ('user', 'permission')

    def __str__(self):
        status = "granted" if self.granted else "denied"
        return f"{self.user.username} - {self.permission.name} ({status})"

class UserThemePreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='theme_preference')
    
    # Theme settings
    primary_color = models.CharField(max_length=7, default='#3498db')  # Default blue
    secondary_color = models.CharField(max_length=7, default='#2c3e50')  # Default dark blue
    accent_color = models.CharField(max_length=7, default='#e74c3c')  # Default red
    background_color = models.CharField(max_length=7, default='#f8f9fa')  # Default light gray
    text_color = models.CharField(max_length=7, default='#343a40')  # Default dark gray
    sidebar_color = models.CharField(max_length=7, default='#2c3e50')  # Default dark blue
    card_color = models.CharField(max_length=7, default='#ffffff')  # Default white
    
    # Theme mode
    THEME_MODE_CHOICES = (
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('custom', 'Custom'),
    )
    theme_mode = models.CharField(max_length=10, choices=THEME_MODE_CHOICES, default='light')
    
    # CSS variables for advanced customization
    custom_css = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Theme Preferences"

    def __str__(self):
        return f"{self.user.username} - Theme Preferences"