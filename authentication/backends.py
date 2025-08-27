from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

User = get_user_model()


class NationalIDBackend(BaseBackend):
    """
    Custom authentication backend that authenticates users using their National ID.
    No password is required - only National ID validation.
    """
    
    def authenticate(self, request, national_id=None, **kwargs):
        if national_id is None:
            return None
        
        try:
            user = User.objects.get(national_id=national_id, is_active=True)
            
            # Check if user is locked due to too many failed attempts
            if user.is_locked():
                return None
            
            # Reset failed attempts on successful authentication
            user.reset_failed_attempts()
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            return user
            
        except User.DoesNotExist:
            # Increment failed attempts for existing users if national_id exists
            try:
                user = User.objects.get(national_id=national_id)
                user.increment_failed_attempts()
            except User.DoesNotExist:
                pass
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None