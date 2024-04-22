from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from register.models import CustomUser
from django.contrib.postgres.fields import ArrayField
from register.models import Group


class Plan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='plansmadefor')
    creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='plansmadeby', blank=True,null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group',blank=True,null=True)    
    subject = models.CharField(max_length=100,blank=True,null=True)
    source = models.CharField(max_length=100)
    destination = ArrayField(models.CharField(max_length=100))
    startTime = models.TimeField()
    endTime = models.TimeField()
    startDate = models.DateField()
    endDate = models.DateField()
    purpose = models.CharField(max_length=100, default="Daily Life Travelling")

    def __str__(self):
        return self.user



