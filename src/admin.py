from django.contrib import admin
from .models import CustomUser, ContactUs, Newsletter, Story,  Comment, Like, Event, Service, Partner, JobOpportunity, JobApplication, TalentProfile, ClientProfile

# Custom admin classes for each model
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_client', 'is_talent')

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address', 'message')
    search_fields = ('first_name', 'last_name', 'email_address')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address')
    search_fields = ('first_name', 'last_name', 'email_address')

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

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'event_name', 'date', 'location', 'start_time', 'end_time')
    search_fields = ('event_name', 'location')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'service_name')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'hiring_company', 'tag')
    search_fields = ('title', 'hiring_company', 'tag')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_opportunity', 'talent', 'applied_date')
    search_fields = ('job_opportunity__title', 'talent__user__email')

@admin.register(TalentProfile)
class TalentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number')
    search_fields = ('user__email', 'address', 'phone_number')

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)

# You can continue to register admins for other models similarly
