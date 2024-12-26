from django import forms
from .models import Employer,Job,JobSkills
from django.core.exceptions import ValidationError

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name','company_logo','company_website','company_description','company_location','employer_email','employer_contact','company_start_date','linkedin_url','company_size','is_hiring']

        widgets = {
            'company_start_date':forms.DateInput(attrs={'type': 'date'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Enter company name'}),
            'company_website': forms.URLInput(attrs={'placeholder':'Enter company webiste'}),
            'company_description': forms.Textarea(attrs={'placeholder':'Provide description of company'}),
            'company_location':forms.TextInput(attrs={'placeholder':'Enter company location'}),
            'employer_email':forms.EmailInput(attrs={'placeholder':'Enter employer email'}),
            'employer_contact':forms.TextInput(attrs={'placeholder':'Enter employer contact number'}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': "Enter Linkedin Url"}),
            'is_hiring': forms.CheckboxInput(attrs={'placeholder':'Is the company currently hiring?'}),
            'company_size': forms.TextInput(attrs={'placeholder':'Enter company size'})
        }

        def clean(self):
            cleaned_data = super().clean()
            fields = ['company_name','company_logo','company_website','company_description','company_location','employer_email','employer_contact','company_start_date','linkedin_url','company_size','is_hiring']

            for data in fields:
                if not cleaned_data(data):
                    raise ValidationError('Please fill the fields')
            return cleaned_data 

class JobForm(forms.ModelForm):
    skills_required = forms.ModelMultipleChoiceField(
        queryset=JobSkills.objects.all(),
        widget = forms.SelectMultiple(),
        required=True
    )

    last_date_to_apply = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)


    class Meta:
        model = Job
        fields = ['title','description','location','salary_range','work_mode','experience','benefits','application_deadline','job_category','role','number_of_openings','status','skills_required']

        widgets = {
            'application_deadline': forms.DateInput(attrs={'type':'date'}),
            'title': forms.TextInput(attrs={'placeholder':"Software Developer - Python"}),
            'description': forms.Textarea(attrs={'placeholder': "Enter job description"}),
            'location': forms.TextInput(attrs={'placeholder':"State/City"}),
            'role': forms.TextInput(attrs={'placeholder':"Enter job role"}),
            'experience': forms.TextInput(attrs={'placeholder':"Enter job experience in digits"}),
            'benefits': forms.Textarea(attrs={'placeholder':"Enter any benefits provided by company"}),
            'skills_required': forms.TextInput(attrs={'placeholder':"Enter job skills"}),
            'job_category': forms.TextInput(attrs={'placeholder':"Enter job category"})
        }