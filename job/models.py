from django.db import models
from src.models import TalentProfile
# Create your models here.

class JobOpportunity(models.Model):
    is_approved = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True, null = True, blank = True)
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
    job_opportunity = models.ForeignKey('JobOpportunity', on_delete=models.CASCADE)
    talent = models.ForeignKey(TalentProfile, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
