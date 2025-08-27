from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from administration.models import Interface, UserInterfaceAccess


def require_interface_access(interface_name=None, module_name=None):
    """
    Decorator to require specific interface access for a view.
    
    Args:
        interface_name: The name of the interface to check
        module_name: The module name to check (alternative to interface_name)
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('authentication:login')
            
            # Admin users have access to everything
            if request.user.is_admin:
                return view_func(request, *args, **kwargs)
            
            try:
                # Find the interface
                if interface_name:
                    interface = Interface.objects.get(function=interface_name)
                elif module_name:
                    interface = Interface.objects.get(module_name=module_name)
                else:
                    # Try to match by URL
                    interface = Interface.objects.get(url=request.path_info)
                
                # Check user access
                try:
                    access = UserInterfaceAccess.objects.get(
                        user=request.user,
                        interface=interface
                    )
                    
                    if not access.has_access:
                        messages.error(request, f'You do not have access to {interface.module_name}.')
                        return redirect('authentication:dashboard')
                        
                except UserInterfaceAccess.DoesNotExist:
                    messages.error(request, f'You do not have access to {interface.module_name}.')
                    return redirect('authentication:dashboard')
                    
            except Interface.DoesNotExist:
                # Interface not found, deny access for security
                messages.error(request, 'Access denied: Interface not found.')
                return redirect('authentication:dashboard')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorator to require admin access for a view.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('authentication:login')
        
        if not request.user.is_admin:
            messages.error(request, 'You must be an administrator to access this page.')
            return redirect('authentication:dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def staff_required(view_func):
    """
    Decorator to require staff access for a view.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('authentication:login')
        
        if not (request.user.is_staff or request.user.is_admin):
            messages.error(request, 'You must be a staff member to access this page.')
            return redirect('authentication:dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def check_interface_access(user, interface_name=None, module_name=None, url=None):
    """
    Utility function to check if a user has access to a specific interface.
    
    Args:
        user: The user to check
        interface_name: The interface function name
        module_name: The module name
        url: The URL pattern
    
    Returns:
        bool: True if user has access, False otherwise
    """
    if not user.is_authenticated:
        return False
    
    # Admin users have access to everything
    if user.is_admin:
        return True
    
    try:
        # Find the interface
        if interface_name:
            interface = Interface.objects.get(function=interface_name)
        elif module_name:
            interface = Interface.objects.get(module_name=module_name)
        elif url:
            interface = Interface.objects.get(url=url)
        else:
            return False
        
        # Check user access
        try:
            access = UserInterfaceAccess.objects.get(
                user=user,
                interface=interface
            )
            return access.has_access
            
        except UserInterfaceAccess.DoesNotExist:
            return False
            
    except Interface.DoesNotExist:
        return False


def get_user_interfaces(user):
    """
    Get all interfaces that a user has access to.
    
    Args:
        user: The user to check
    
    Returns:
        QuerySet: Interfaces the user has access to
    """
    if not user.is_authenticated:
        return Interface.objects.none()
    
    # Admin users have access to all interfaces
    if user.is_admin:
        return Interface.objects.all()
    
    # Get interfaces where user has access
    accessible_interfaces = UserInterfaceAccess.objects.filter(
        user=user,
        has_access=True
    ).values_list('interface', flat=True)
    
    return Interface.objects.filter(interface_id__in=accessible_interfaces)