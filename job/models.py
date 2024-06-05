from django.db import models

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

    def __str__(self):
        return self.title + " | " + self.hiring_company

class JobApplication(models.Model):
    job_opportunity = models.ForeignKey('JobOpportunity', on_delete=models.CASCADE)
    talent = models.ForeignKey('src.TalentProfile', on_delete=models.CASCADE, related_name='talentprofile')
    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_opportunity} applied by {self.talent} on {self.applied_date}"

