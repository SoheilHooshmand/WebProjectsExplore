from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender = User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )

@receiver(post_delete, sender=Profile)
def deleteProfile(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    # print(f"User {instance} deleted by {sender}")


@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# @receiver(post_save, sender=Profile)
# def profileUpdate(sender, instance, created, **kwargs):
#     print("Profile saved")
#     print(f"sender: {sender}")
#     print(f"instance: {instance}")
#     print(f"created: {created}")
#


# post_save.connect(profileUpdate, sender=Profile)
# post_delete.connect(deleteProfile, sender=Profile)