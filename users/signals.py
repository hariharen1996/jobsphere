from django.db.models.signals import post_save,post_migrate
from django.dispatch import receiver 
from django.contrib.auth import get_user_model 
from .models import Profile


CustomUser = get_user_model()

@receiver(post_save,sender=CustomUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=CustomUser)
def save_profile(sender,instance,**kwargs):
    if hasattr(instance,'profile'):
        instance.profile.save()

@receiver(post_migrate)
def create_existing_user_profile(sender,**kwargs):
    user_profile = CustomUser.objects.filter(profile__isnull=True)
    for user in user_profile:
        Profile.objects.create(user=user)        