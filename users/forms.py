from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser,Profile,Skill,Certification
from django import forms
from django.core.exceptions import ValidationError
import re

WIDGETS = {
    'username': {'placeholder': "Enter your username"},
    'email': {'placeholder': "Enter your email address"},
    'password': {'placeholder': "Enter your Password"},
    'password_confirm': {'placeholder': "Confirm your Password"},
    'bio': {'placeholder': 'Tell us about yourself', 'rows': 5, 'cols': 30},
    'location': {'placeholder': 'Enter your location - state/city'},
    'education': {'placeholder': 'Enter your recent education'},
    'work_experience': {'placeholder': 'Describe your work experience', 'rows': 5, 'cols': 40},
    'cgpa': {'placeholder': 'Enter your CGPA'},
    'certification_name': {'placeholder': "Enter certification name"}
}


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs=WIDGETS['email']))
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES,label='Account')

    
    username = forms.CharField(widget=forms.TextInput(attrs=WIDGETS['username']))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs=WIDGETS['password']))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=WIDGETS['password_confirm']))
    

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



class CustomUserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs=WIDGETS['username']))
    email = forms.EmailField(widget=forms.TextInput(attrs=WIDGETS['email']))


    class Meta:
        model = CustomUser
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(),
        required=True
    )

    certifications = forms.ModelMultipleChoiceField(
        queryset=Certification.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    certification_name = forms.CharField(
        max_length=255,
        label="Certification Name",
        widget=forms.TextInput(attrs=WIDGETS['certification_name']),
        required=False 
    )

    certification_image = forms.ImageField(
        label="Upload certification image",
        required=False 
    )

    resume = forms.FileField(
        label="Upload Resume",
        required=True
    )

    class Meta:
        model = Profile 
        fields = ['image','bio','skills','education','cgpa','work_experience','resume','location','certifications','certification_name','certification_image']
        widgets = {
            'bio': forms.Textarea(attrs=WIDGETS['bio']),
            'location': forms.TextInput(attrs=WIDGETS['location']),
            'education': forms.TimeInput(attrs=WIDGETS['education']),
            'work_experience': forms.Textarea(attrs=WIDGETS['work_experience']),
            'cgpa': forms.NumberInput(attrs=WIDGETS['cgpa'])
        }

    def save(self,commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        
        skills = self.cleaned_data.get('skills')
        if skills:
            profile.skills.set(skills)
        
        certifications = self.cleaned_data.get('certifications')
        if certifications:
            profile.certification.set(certifications)
        
        certification_name = self.cleaned_data.get('certification_name')
        certification_image = self.cleaned_data.get('certification_image')
        
        if certification_name and certification_image:
            certification = Certification.objects.create(name=certification_name,cert_image=certification_image)
            profile.certification.add(certification)
        
        resume = self.cleaned_data.get('resume')
        if resume:
            profile.resume = resume 
        
        profile.save()

        return profile
    
    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if bio and len(bio) > 1000:
            raise forms.ValidationError('Bio should not exceed 1000 characters')
        return bio 
    
    def clean_cgpa(self):
        cgpa = self.cleaned_data.get('cgpa')
        if cgpa and (cgpa < 0.0 and cgpa > 10.0):
            raise forms.ValidationError('cgpa must be between 0.00 and 10.00')

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and not resume.name.endswith('.pdf'):
            raise forms.ValidationError('Resume must be a pdf file')
        return resume

    def clean_certification_image(self):
        certification_image = self.cleaned_data.get('certification_image')
        if certification_image:
            if not certification_image.name.endswith(('.png','.jpg','.jpeg')):
                raise forms.ValidationError('Only jpg,png,jpeg files are allowed') 
        return certification_image   
    
    def clean_certifications(self):
        certifications = self.cleaned_data.get('certifications')
        if certifications and len(certifications) > 5:
            raise forms.ValidationError('A profile can have only upto 5 certifications')
        return certifications

    def clean(self):
        return super().clean()