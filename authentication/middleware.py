from django.shortcuts import redirect
from django.contrib import messages
from django.urls import resolve
from django.http import HttpResponseForbidden
from administration.models import Interface, UserInterfaceAccess


class InterfaceAccessMiddleware:
    """
    Middleware to check if users have access to specific interfaces
    based on the URL patterns and their assigned interface permissions.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that don't require interface access control
        self.exempt_urls = [
            'authentication:login',
            'authentication:logout',
            'authentication:dashboard',
            'admin:index',  # Django admin
        ]
        
        # URLs that require admin access
        self.admin_only_urls = [
            'administration:',  # All administration URLs
        ]
    
    def __call__(self, request):
        # Process the request before the view
        if request.user.is_authenticated:
            self.check_interface_access(request)
        
        response = self.get_response(request)
        return response
    
    def check_interface_access(self, request):
        """
        Check if the current user has access to the requested interface
        """
        try:
            # Get the current URL name
            resolved = resolve(request.path_info)
            url_name = f"{resolved.namespace}:{resolved.url_name}" if resolved.namespace else resolved.url_name
            
            # Skip access control for exempt URLs
            if any(exempt in url_name for exempt in self.exempt_urls):
                return
            
            # Check if user is admin for admin-only URLs
            if any(admin_url in url_name for admin_url in self.admin_only_urls):
                if not request.user.is_admin:
                    messages.error(request, 'You do not have permission to access this area.')
                    return redirect('authentication:dashboard')
                return
            
            # Check interface-specific access
            try:
                interface = Interface.objects.get(url=request.path_info)
                
                # Check if user has access to this interface
                try:
                    access = UserInterfaceAccess.objects.get(
                        user=request.user,
                        interface=interface
                    )
                    
                    if not access.has_access:
                        messages.error(request, f'You do not have access to {interface.module_name}.')
                        return redirect('authentication:dashboard')
                        
                except UserInterfaceAccess.DoesNotExist:
                    # No access record means no access
                    messages.error(request, f'You do not have access to {interface.module_name}.')
                    return redirect('authentication:dashboard')
                    
            except Interface.DoesNotExist:
                # Interface not defined, allow access for now
                # This allows for gradual implementation of interface control
                pass
                
        except Exception as e:
            # Log the error in production
            # For now, allow access to prevent breaking the system
            pass


class SessionTimeoutMiddleware:
    """
    Middleware to handle session timeout for security
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Session timeout in seconds (30 minutes)
        self.session_timeout = 30 * 60
    
    def __call__(self, request):
        if request.user.is_authenticated:
            self.check_session_timeout(request)
        
        response = self.get_response(request)
        return response
    
    def check_session_timeout(self, request):
        """
        Check if the session has timed out
        """
        from django.utils import timezone
        from django.contrib.auth import logout
        
        last_activity = request.session.get('last_activity')
        
        if last_activity:
            # Convert string back to datetime if needed
            if isinstance(last_activity, str):
                from datetime import datetime
                last_activity = datetime.fromisoformat(last_activity)
            
            # Check if session has expired
            if (timezone.now() - last_activity).total_seconds() > self.session_timeout:
                logout(request)
                messages.warning(request, 'Your session has expired. Please log in again.')
                return redirect('authentication:login')
        
        # Update last activity
        request.session['last_activity'] = timezone.now().isoformat()