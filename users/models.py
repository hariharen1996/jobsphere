from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Applicant','Applicant'),
        ('Recruiter','Recruiter')
    )

    user_type = models.CharField(max_length=20,choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pic')

    def __str__(self):
        return f"{self.user.username} profile"