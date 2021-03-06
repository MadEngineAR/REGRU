from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)
    age = models.PositiveIntegerField(default=18)

    activation_key = models.CharField(max_length=120, blank=True)
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)

    def is_activation_key_expires(self):
        if now() <= self.activation_key_expires + timedelta(hours=48):
            return False
        else:
            return True


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOISES = (
        (MALE, 'M'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(User, unique=True,null=True,db_index=True,on_delete=models.CASCADE)
    about = models.TextField(verbose_name='О себе', blank=True, null=False)
    gender = models.CharField(verbose_name='Пол', choices=GENDER_CHOISES, blank=True, max_length=2)
    langs = models.CharField(verbose_name='Язык', blank=True, max_length=10, default='RU')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created,**kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if not created:
            instance.userprofile.save()
