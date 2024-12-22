from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError
import re

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder':'Enter your email address'}))
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES,label='Account')

    
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your username"}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter your Password"}))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm your Password"}))
    

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

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'placeholder':'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))