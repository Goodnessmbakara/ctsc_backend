from django.contrib import admin
from .models import CustomUser, ContactUs, Newsletter, Event, Service, Partner, TalentProfile, ClientProfile

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


@admin.register(TalentProfile)
class TalentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number')
    search_fields = ('user__email', 'address', 'phone_number')

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)

# You can continue to register admins for other models similarly
