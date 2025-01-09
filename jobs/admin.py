from django.contrib import admin
from .models import Employer,Job,JobApplicationSkills,Review,Reply,JobApplication

# Register your models here.
admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(JobApplicationSkills)
admin.site.register(Review)
admin.site.register(Reply)
