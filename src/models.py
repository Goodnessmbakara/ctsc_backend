from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver




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
    profile_pics = models.ImageField(upload_to='profile_pics')
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

class Story(models.Model):
    story_id = models.AutoField(primary_key=True)
    is_currently_featured = models.BooleanField(default=False, null =True, blank =True)
    featured_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length = 100)
    author = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING, null = True, blank = True)
    image = models.ImageField(upload_to = 'story_images')
    short_description = models.CharField(max_length = 255)
    body = models.TextField()

    @classmethod
    def get_latest_featured_story(cls):
        return cls.objects.filter(is_currently_featured=True).order_by('-featured_date').first()

    @classmethod
    def get_previous_featured_stories(cls):
        return cls.objects.filter(is_currently_featured=False, featured_date__isnull=False).order_by('-featured_date')

    def save(self, *args, **kwargs):
        if self.is_currently_featured:
            # Check if there is a currently featured story, if so, set it to not featured
            previous_featured = Story.get_latest_featured_story()
            if previous_featured:
                previous_featured.is_currently_featured = False
                previous_featured.save()
            # Set the new story as the currently featured story
            self.is_currently_featured = True
            self.featured_date = timezone.now()

        super().save(*args, **kwargs)


class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser,null=True, on_delete=models.SET_NULL)
    comment_body = models.TextField()
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete = models.CASCADE)

    def likes_count(self):
        self.likes.count()

class Like(models.Model):
    comment = models.OneToOneField('Comment', on_delete=models.CASCADE, related_name = 'likes')
    count = models.PositiveIntegerField(default = 0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null = True)

    class Meta:
        unique_together = ('comment', 'user')

class Event(models.Model):
    event_id = models.PositiveIntegerField(primary_key = True, unique = True)
    event_image = models.ImageField(upload_to = 'event_images')
    event_name = models.CharField(max_length = 60)
    date = models.DateField()
    location = models.CharField(max_length = 255)
    registation_link = models.URLField()
    about = models.CharField(max_length  = 100)
    brief_summary  = models.CharField(max_length  = 255)
    start_time = models. DateTimeField()
    end_time = models. DateTimeField()

class Service(models.Model):
    service_id = models.PositiveIntegerField(primary_key = True, unique = True)
    service_name = models.CharField(max_length = 50)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING, related_name = 'sender')
    recipient  = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING, related_name = 'receiver')
    message_file = models.FileField(null = True, blank =True)
    image = models.ImageField(null = True, blank =True)
    text = models.TextField(null = True, blank =True)

class Partner(models.Model):
    partner_pics = models.ImageField()
    name = models.CharField(max_length = 50)
    description = models.TextField()

class JobOpportunity(models.Model):
    category = models.CharField(max_length = 50)
    title = models.CharField(max_length=200)
    hiring_company = models.CharField(max_length=200)
    TAG_CHOICES = [
        ('Remote', 'Remote'),
        ('Onsite', 'Onsite'),
        ('Hybrid', 'Hybrid'),
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
    ]
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)
    requirements = models.TextField()

class JobApplication(models.Model):
    job_opportunity = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE)
    talent = models.ForeignKey('TalentProfile', on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)

class TalentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
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
