from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError
import re

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder':'Enter your email address'}),help_text="Enter a valid email address")
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES,label='Account',help_text="Select the type of account you want to create")

    class Meta:
        model = CustomUser
        fields = ['username','email','user_type','password1','password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.search(r'[A-Z]',password):
            raise ValidationError('Password must contain atleat one uppercase letter')
        if not re.search(r'[0-9]',password):
            raise ValidationError('Password must contain atleast one digit')
        if not re.search(r'[@#$!%*?&^()]',password):
            raise ValidationError('Password must contain atleast one special character')
        if not re.search(r'[a-z]',password):
            raise ValidationError('Password must contain atleast one lowercase letter')