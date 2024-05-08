from django.contrib import admin
from .models import Message
# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'text')
    search_fields = ('sender__email', 'recipient__email', 'text')