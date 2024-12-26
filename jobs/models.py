from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import RegexValidator
from datetime import date

CustomUser = get_user_model()

# Create your models here.
class Employer(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,unique=True)
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to="company_logo/")
    company_website = models.URLField(blank=True,null=True)
    company_description = models.TextField()
    company_location = models.CharField(max_length=255)
    employer_email = models.EmailField()
    employer_contact = models.CharField(max_length=15,blank=True,null=True,validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")])
    company_start_date = models.DateField(blank=True,null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    company_size = models.CharField(max_length=100, blank=True, null=True)
    is_hiring = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}"
    

class JobSkills(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name    

class Job(models.Model):
    SALARY_CHOICES = (
        ('0-3','0-3 Lakhs'),
        ('3-6','3-6 Lakhs'),
        ('6-10','6-10 Lakhs'),
        ('10-15','10-15 Lakhs'),
        ('15-20','15-20 Lakhs'),
        ('20+','20+ Lakhs'),
    )

    WORK_MODE_CHOICES = (
        ('wfo',"Work from Office"),
        ('hybrid','Hybrid'),
        ('remote','Remote')
    )

    FRESHNESS_CHOICES = (
        (0, 'Freshness'),
        (1, 'Last 1 Day'),
        (3, 'Last 3 Days'),
        (7, 'Last 7 Days'),
        (15, 'Last 15 Days'),
        (30, 'Last 30 Days'),
    )

    JOB_STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('filled', 'Filled'),
    )

    EXPERIENCE_CHOICES = (
        ('0-2', '0-2 years'),
        ('3-6', '3-6 years'),
        ('7-10', '7-10 years'),
        ('10+', '10+ years'),
    )

    employer = models.ForeignKey(Employer,on_delete=models.CASCADE,related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary_range = models.CharField(max_length=5,choices=SALARY_CHOICES,default='0-3')
    work_mode = models.CharField(max_length=10,choices=WORK_MODE_CHOICES,default="wfo")
    role = models.CharField(max_length=255)
    experience = models.CharField(max_length=5,choices=EXPERIENCE_CHOICES,default='0-2')
    time_range = models.IntegerField(choices=FRESHNESS_CHOICES,default=0)
    created_at = models.DateTimeField(default=timezone.now)
    posted_time = models.DateTimeField(auto_now_add=True)
    benefits = models.TextField(blank=True, null=True)
    application_deadline = models.DateField(blank=False, null=False,default=date(2024, 12, 30))
    job_category = models.CharField(max_length=100, blank=False, null=False,default="Development")
    number_of_openings = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=JOB_STATUS_CHOICES, default='open')
    skills_required = models.ManyToManyField(JobSkills,blank=False)



    def __str__(self):
        return f"{self.title}"