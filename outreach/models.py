# models.py
from django.db import models

class OutreachBatch(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

class Photo(models.Model):
    outreach_batch = models.ForeignKey(OutreachBatch, related_name='photos', on_delete=models.CASCADE, db_index=True)
    image = models.ImageField(upload_to='outreach_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Video(models.Model):
    outreach_batch = models.ForeignKey(OutreachBatch, related_name='videos', on_delete=models.CASCADE, db_index=True)
    video = models.FileField(upload_to='outreach_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)