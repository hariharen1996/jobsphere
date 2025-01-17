from django.contrib import admin
from .models import Employer,Job,JobApplicationSkills,Review,Reply,JobApplication,JobSkills

# Register your models here.
admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(JobApplicationSkills)
admin.site.register(JobSkills)
admin.site.register(Review)
admin.site.register(Reply)
