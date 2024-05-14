from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ContactUs, Newsletter, Event, Service, Partner, TalentProfile, ClientProfile, TeamMember

# Custom admin for CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_client', 'is_talent')
    list_filter = ('is_staff', 'is_active', 'is_client', 'is_talent')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_client', 'is_talent')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_client', 'is_talent'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)



# Custom managers for TalentProfile and ClientProfile
class TalentProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user')

class ClientProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user')

# Model admins for TalentProfile and ClientProfile
@admin.register(TalentProfile)
class TalentProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'address', 'phone_number')
    search_fields = ('user__email', 'address', 'phone_number')
    list_filter = ('services',)

    def user_email(self, obj):
        return obj.user.email

    user_email.admin_order_field = 'user__email'

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'address', 'phone_number')
    search_fields = ('user__email', 'address', 'phone_number')

    def user_email(self, obj):
        return obj.user.email

    user_email.admin_order_field = 'user__email'

# Register models with their respective admins
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ContactUs)
admin.site.register(Newsletter)
admin.site.register(Event)
admin.site.register(Service)
admin.site.register(Partner)
admin.site.register(TeamMember)