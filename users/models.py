from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Applicant','Applicant'),
        ('Recruiter','Recruiter')
    )

    user_type = models.CharField(max_length=20,choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username
    

class Certification(models.Model):
    name = models.CharField(max_length=255)
    cert_image = models.ImageField(upload_to='certifications/')

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"

    def __str__(self):
        return self.name

class SkillCategory(models.Model):
    name = models.CharField(max_length=100,unique=True)

    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(SkillCategory,on_delete=models.CASCADE,related_name="skills",default=1)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name','category'],name="unique_skill_category")
        ]

    def __str__(self):
        return self.name   

class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pic')
    bio = models.TextField(default="I am Hari...")
    education = models.CharField(max_length=255,blank=False,null=False,default="ABC institute of technology")
    cgpa = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,default=0.0)
    work_experience = models.TextField(default="No work experince available")
    resume = models.FileField(upload_to='resumes/',default="resumes/default_resume.pdf")
    location = models.CharField(max_length=255,default="TamilNadu/Chennai")
    certification = models.ManyToManyField(Certification,related_name='profiles')
    skills = models.ManyToManyField(Skill)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def clean(self):
        total_cert = self.certification.count()

        if total_cert > 5:
            raise ValidationError('A profile can only have 5 certifications')   

    def __str__(self):
        return f"{self.user.username} profile"