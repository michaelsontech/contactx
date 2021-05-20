from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a user with the given email, first name, 
        last name and password
        """
        if not email:
            raise ValueError('Users must have an email')
        # if not first_name:
        #     raise ValueError('Users must have a first name')
        # if not last_name:
        #     raise ValueError('Users must have a last name')

        user = self.model(
            email = email, 
            first_name = first_name,
            last_name = last_name,            
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, first name, 
        last name and password
        """
        user = self.create_user(
            email,
            first_name, 
            last_name,             
            password
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True 
        user.save()
        return user


class Account(AbstractBaseUser):

    email = models.EmailField(verbose_name='email', max_length=255, unique=True)    
    phone_number = PhoneNumberField(verbose_name='phone', unique=True, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    date_created = models.DateTimeField(verbose_name='date created', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):        
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


