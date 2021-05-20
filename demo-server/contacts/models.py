from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
  """ DB model for storing users contacts"""

  full_name = models.CharField(max_length=255)
  phone_number = phone_number = PhoneNumberField(verbose_name='phone_number', null=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
