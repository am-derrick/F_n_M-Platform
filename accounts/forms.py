from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    """Form for new user sign up"""
    usable_password = None
    email = forms.CharField(max_length=254, required=True,
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')