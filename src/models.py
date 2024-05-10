from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default = False)
    is_talent = models.BooleanField(default = False)
    profile_pics = CloudinaryField('image', null=True, blank=True)
    address = models.CharField(max_length = 255)
    phone_number = models.CharField(max_length = 20)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ContactUs(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.CharField(max_length=100)
    message = models.TextField()

class Newsletter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.CharField(max_length=100)


class Event(models.Model):
    event_id = models.AutoField(primary_key = True)
    event_image = CloudinaryField('image', null=True, blank=True)
    event_name = models.CharField(max_length = 60)
    date = models.DateField()
    location = models.CharField(max_length = 255)
    registation_link = models.URLField()
    about = models.CharField(max_length  = 100)
    brief_summary  = models.CharField(max_length  = 255)
    start_time = models. DateTimeField()
    end_time = models. DateTimeField()

class Service(models.Model):
    service_id = models.AutoField(primary_key = True)
    service_name = models.CharField(max_length = 50)

class Partner(models.Model):
    partner_pics = CloudinaryField('image', null=True, blank=True)
    name = models.CharField(max_length = 50)
    description = models.TextField()

class TalentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = CloudinaryField('image', blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

class ClientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)

class TeamMember(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    about = models.CharField(max_length = 100)
    profile_image = models.ImageField(upload_to = 'team_member/')

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:  # Only execute if a new instance is created
        if instance.is_client:
            ClientProfile.objects.create(user=instance)
        else:
            TalentProfile.objects.create(user=instance)
