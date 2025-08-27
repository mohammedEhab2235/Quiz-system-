from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class NationalIDLoginForm(forms.Form):
    national_id = forms.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{14}$',
                message='National ID must be exactly 14 digits.'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your 14-digit National ID',
            'autofocus': True,
            'maxlength': '14',
            'pattern': '[0-9]{14}',
            'title': 'Please enter exactly 14 digits'
        })
    )
    
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
    
    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        
        if national_id:
            # Check if user exists and is active
            try:
                user = User.objects.get(national_id=national_id)
                if not user.is_active:
                    raise forms.ValidationError(
                        'This account has been deactivated. Please contact an administrator.'
                    )
                if user.is_locked():
                    raise forms.ValidationError(
                        'This account has been locked due to too many failed login attempts. '
                        'Please contact an administrator.'
                    )
            except User.DoesNotExist:
                raise forms.ValidationError(
                    'Invalid National ID. Please check your ID and try again.'
                )
        
        return national_id
    
    def clean(self):
        national_id = self.cleaned_data.get('national_id')
        
        if national_id:
            self.user_cache = authenticate(
                self.request,
                national_id=national_id
            )
            if self.user_cache is None:
                # Try to get the user to increment failed attempts
                try:
                    user = User.objects.get(national_id=national_id)
                    user.increment_failed_attempts()
                except User.DoesNotExist:
                    pass
                
                raise forms.ValidationError(
                    'Authentication failed. Please check your National ID.'
                )
        
        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache


class UserCreationForm(forms.ModelForm):
    """Form for creating new users by administrators"""
    
    class Meta:
        model = User
        fields = ('national_id', 'name', 'position', 'phone_number', 'is_active', 'is_admin')
        widgets = {
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '14-digit National ID',
                'maxlength': '14',
                'pattern': '[0-9]{14}'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Position'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_admin': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  # No password authentication
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating existing users by administrators"""
    
    class Meta:
        model = User
        fields = ('name', 'position', 'phone_number', 'is_active', 'is_admin')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_admin': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }