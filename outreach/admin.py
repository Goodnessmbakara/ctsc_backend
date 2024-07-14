# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import OutreachBatch, Photo, Video

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    readonly_fields = ('video_preview',)

    def video_preview(self, obj):
        if obj.video:
            return format_html('<video width="200" height="200" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
        return "No Video"
    video_preview.short_description = 'Preview'

@admin.register(OutreachBatch)
class OutreachBatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'created_at', 'updated_at', 'photo_count', 'video_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('description',)
    date_hierarchy = 'created_at'
    inlines = [PhotoInline, VideoInline]

    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Photos'

    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videos'

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'outreach_batch', 'image_preview', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('outreach_batch__description',)
    date_hierarchy = 'uploaded_at'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'outreach_batch', 'video_preview', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('outreach_batch__description',)
    date_hierarchy = 'uploaded_at'

    def video_preview(self, obj):
        if obj.video:
            return format_html('<video width="200" height="200" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>', obj.video.url)
        return "No Video"
    video_preview.short_description = 'Preview'