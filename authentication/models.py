from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, national_id, name, **extra_fields):
        if not national_id:
            raise ValueError('The National ID must be set')
        if not name:
            raise ValueError('The Name must be set')
        
        user = self.model(
            national_id=national_id,
            name=name,
            **extra_fields
        )
        user.set_unusable_password()  # No password authentication
        user.save(using=self._db)
        return user

    def create_superuser(self, national_id, name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(national_id, name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    national_id_validator = RegexValidator(
        regex=r'^[0-9]{14}$',
        message='National ID must be exactly 14 digits.'
    )
    
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
    )
    
    national_id = models.CharField(
        max_length=14,
        unique=True,
        validators=[national_id_validator],
        help_text='14-digit National ID'
    )
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(
        max_length=17,
        validators=[phone_validator],
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.name} ({self.national_id})"
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name
    
    def reset_failed_attempts(self):
        self.failed_login_attempts = 0
        self.save(update_fields=['failed_login_attempts'])
    
    def increment_failed_attempts(self):
        self.failed_login_attempts += 1
        self.last_login_attempt = timezone.now()
        self.save(update_fields=['failed_login_attempts', 'last_login_attempt'])
    
    def is_locked(self):
        from django.conf import settings
        return self.failed_login_attempts >= getattr(settings, 'MAX_LOGIN_ATTEMPTS', 5)
