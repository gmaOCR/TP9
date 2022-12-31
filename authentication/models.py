from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # CREATOR = 'CREATOR'
    # DEV = 'DEVELOPER'
    #
    # ROLE_CHOICES = (
    #     (CREATOR, 'Créateur'),
    #     (DEV, 'Dev'),
    # )
    # profile_photo = models.ImageField(verbose_name='photo de profil')
    # role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='rôle')
    # follows = models.ManyToManyField(
    #     'self',
    #     limit_choices_to={'role': CREATOR},
    #     symmetrical=False,
    #     verbose_name='suit'
    # )
    #
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.role == self.CREATOR:
    #         group = Group.objects.get(name='creators')
    #         group.user_set.add(self)
    #     elif self.role == self.SUBSCRIBER:
    #         group = Group.objects.get(name='subscribers')
    #         group.user_set.add(self)
