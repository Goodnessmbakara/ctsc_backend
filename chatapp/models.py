from django.db import models
from django.conf import settings
from datetime import timezone

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    #message_type = models.CharField(max_length=10, choices=['text', 'document', 'picture', 'audio', 'video'])
    message = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='messages/files/', blank=True)
    timestamp = models.DateTimeField(auto_now_add = True, null = True)
    read_receipt = models.BooleanField(default=False)
    
    def __str__(self):
        return self.message
    