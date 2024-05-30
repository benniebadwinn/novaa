from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile




# from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
# from django.dispatch import receiver
from .models import UserProfuile

user = get_user_model()





@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)









@receiver(post_save, sender=user)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfuile.objects.create(user=instance)
