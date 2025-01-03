from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import RegexValidator
from datetime import date
from users.models import Skill,Profile

CustomUser = get_user_model()

# Create your models here.
class Employer(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,unique=True)
    employer_image = models.ImageField(upload_to='employer_profile_pic/',default="emp_default.jpg")
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to="company_logo/",null=True,blank=True,default='default_logo.png')
    company_website = models.URLField(blank=True,null=True)
    company_description = models.TextField()
    company_location = models.CharField(max_length=255)
    employer_email = models.EmailField()
    employer_contact = models.CharField(max_length=15,blank=True,null=True,validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")])
    company_start_date = models.DateField(blank=True,null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    company_size = models.CharField(max_length=100, blank=True, null=True)
    is_hiring = models.BooleanField(default=True)

      
    def is_complete(self):
        all_fields = [self.employer_image,self.company_name,self.company_logo,self.company_website,self.company_description,self.company_location,self.employer_email,self.employer_contact,self.company_start_date,self.linkedin_url,self.company_size,self.is_hiring]

        return not any(fields is None or (isinstance(fields,str) and fields.strip() == '') 
                      or (isinstance(fields,list) and len(fields) == 0) for fields in all_fields
                       )


    def __str__(self):
        return f"{self.user.username}"
    
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
        ('WFO',"Work from Office"),
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
        ('0-1', '0-1 years'),
        ('1-3', '1-3 years'),
        ('3-5', '3-5 years'),
        ('5-7', '5-7 years'),
        ('7-10', '7-10 years'),
        ('10+', '10+ years'),
    )

    employer = models.ForeignKey(Employer,on_delete=models.CASCADE,related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=200)
    min_salary = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    max_salary = models.DecimalField(max_digits=10,decimal_places=2,default=3)
    salary_range = models.CharField(max_length=5,choices=SALARY_CHOICES,default='0-3')
    work_mode = models.CharField(max_length=10,choices=WORK_MODE_CHOICES,default="WFO")
    role = models.CharField(max_length=255)
    experience = models.CharField(max_length=5,choices=EXPERIENCE_CHOICES,default='0-1')
    time_range = models.IntegerField(choices=FRESHNESS_CHOICES,default=0)
    created_at = models.DateTimeField(default=timezone.now)
    posted_time = models.DateTimeField(auto_now_add=True)
    benefits = models.TextField(blank=True, null=True)
    application_deadline = models.DateField(blank=False, null=False,default=timezone.now)
    job_category = models.CharField(max_length=100, blank=False, null=False,default="Development/It")
    number_of_openings = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=JOB_STATUS_CHOICES, default='open')
    job_related_skills =  models.ManyToManyField(Skill,related_name='job_skills')

    def save(self,*args,**kwargs):
        if self.salary_range == '0-3':
            self.min_salary = 0
            self.max_salary = 3
        elif self.salary_range == '3-6':
            self.min_salary = 3
            self.max_salary = 6 
        elif self.salary_range == '6-10':
            self.min_salary = 6
            self.max_salary = 10 
        elif self.salary_range == '10-15':
            self.min_salary = 10
            self.max_salary = 15
        elif self.salary_range == '15-20':
            self.min_salary = 15
            self.max_salary = 20
        elif self.salary_range == '20+':
            self.min_salary = 20
            self.max_salary = 100000
        super(Job,self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.title}"

class SavedJob(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
    
class JobApplicationSkills(models.Model):
    job_application_skills = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['job_application_skills'],name="unique_jobapp_skills")
        ]

    def __str__(self):
        return self.job_application_skills    

class JobApplication(models.Model):
    applicant = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE) 
    applied_at = models.DateTimeField(auto_now_add=True)
    jobapplication_skills = models.ManyToManyField(JobApplicationSkills,related_name="job_applications",blank=True)

    class Meta:
        unique_together = ('applicant','job')
    
    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"