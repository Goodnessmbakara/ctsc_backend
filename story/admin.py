from django.contrib import admin

# Register your models here.
from .models import  Story,  Comment, Like

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('story_id', 'topic', 'author', 'created_at', 'is_currently_featured')
    search_fields = ('topic', 'author__email', 'author__first_name', 'author__last_name')
    list_filter = ('is_currently_featured',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment_body', 'reply_to')
    search_fields = ('user__email', 'comment_body')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment')
    search_fields = ('user__email',)