from django.db import models
from django.conf import settings
from django.utils import timezone


class Interface(models.Model):
    interface_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=255, help_text='Name of the interface/module')
    function = models.CharField(max_length=255, help_text='Function or purpose of the interface')
    url = models.CharField(max_length=500, help_text='URL pattern for the interface')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'interfaces'
        verbose_name = 'Interface'
        verbose_name_plural = 'Interfaces'
    
    def __str__(self):
        return f"{self.module_name} - {self.function}"


class UserInterfaceAccess(models.Model):
    access_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interface_access')
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE, related_name='user_access')
    has_access = models.BooleanField(default=False)
    granted_date = models.DateTimeField(default=timezone.now)
    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='granted_access'
    )
    
    class Meta:
        db_table = 'userinterfaceaccess'
        verbose_name = 'User Interface Access'
        verbose_name_plural = 'User Interface Access'
        unique_together = ['user', 'interface']
    
    def __str__(self):
        access_status = 'Granted' if self.has_access else 'Denied'
        return f"{self.user.name} - {self.interface.module_name} - {access_status}"
