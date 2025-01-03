from django.contrib import admin
from .models import Employer,Job,JobApplicationSkills

# Register your models here.
admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(JobApplicationSkills)
