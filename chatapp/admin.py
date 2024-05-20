from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'file', 'timestamp', 'read_receipt')
    list_filter = ('sender', 'receiver', 'read_receipt')
    search_fields = ('message',)
    readonly_fields = ('timestamp',)

    def file(self, obj):
        if obj.file:
            return f'<a href="{obj.file.url}" target="_blank">{obj.file.name}</a>'
        return '-'

    file.allow_tags = True