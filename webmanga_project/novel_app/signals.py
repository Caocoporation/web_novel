from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Novel_Illustration, Novel

@receiver(post_save, sender=Novel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Novel_Illustration.objects.create(novel=instance)

@receiver(post_save, sender=Novel)
def save_profile(sender, instance, **kwargs):
    instance.profile.save() 