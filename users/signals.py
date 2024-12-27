from django.db.models.signals import post_save,post_migrate
from django.dispatch import receiver 
from django.contrib.auth import get_user_model 
from .models import Profile
from jobs.models import Employer


CustomUser = get_user_model()

@receiver(post_save,sender=CustomUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type == 'Applicant':
            Profile.objects.get_or_create(user=instance)
        elif instance.user_type == 'Recruiter':
            Employer.objects.get_or_create(user=instance)


# @receiver(post_save,sender=CustomUser)
# def save_profile(sender,instance,**kwargs):
#     if instance.user_type == 'Applicant' and not hasattr(instance,'profile'):
#         Profile.objects.get_or_create(user=instance)
#     if instance.user_type == 'Employer' and not hasattr(instance,'employer'):
#         Employer.objects.get_or_create(user=instance)
    

@receiver(post_migrate)
def create_existing_user_profile(sender,**kwargs):
    applicant_user_profile = CustomUser.objects.filter(profile__isnull=True,user_type='Applicant')
    for user in applicant_user_profile:
        Profile.objects.get_or_create(user=user)        
    
    recruiter_user_profile = CustomUser.objects.filter(employer__isnull=True,user_type='Recruiter')
    for user in recruiter_user_profile:
        Employer.objects.get_or_create(user=user)        
    