from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser
from django import forms

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder':'Enter your email address'}),help_text="Enter a valid email address")
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES,label='Account',help_text="Select the type of account you want to create")

    class Meta:
        model = CustomUser
        fields = ['username','email','user_type','password1','password2']
