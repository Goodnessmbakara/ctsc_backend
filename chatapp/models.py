from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_file = CloudinaryField('file', null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    audio = CloudinaryField('audio', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank = True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"