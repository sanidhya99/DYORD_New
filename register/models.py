from django.db import models
from .manage import *
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.db.models import F


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=10000,blank=True,null=True)
    image = models.CharField(max_length=1000,blank=True,null=True)
    gender = models.CharField(max_length=20,blank=True,null=True)
    number = models.BigIntegerField(unique=True,blank=True,null=True)
    age = models.BigIntegerField(blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()
    REQUIRED_FIELDS = ["name", "number"]
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class people(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=50, default="Friend")


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(CustomUser, related_name='FriendGroups')

    def __str__(self):
        return self.name


class GroupRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.user
