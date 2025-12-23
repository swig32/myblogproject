from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Member(models.Model):
    # Added the link to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default_avatar.png', blank=True,null=True)
    emailaddress = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True) # CharField for better phone formatting
    joined_date = models.DateField(auto_now_add=True, null=True) # Automatically sets date when they join

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(
            user=instance,
            firstname=instance.first_name or instance.username,
            lastname=instance.last_name,
            emailaddress=instance.email
        )