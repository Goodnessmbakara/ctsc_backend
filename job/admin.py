from django.contrib import admin

from .models import JobApplication, JobOpportunity
# Register your models here.
@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'hiring_company', 'tag')
    search_fields = ('title', 'hiring_company', 'tag')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_opportunity', 'talent', 'applied_date')
    search_fields = ('job_opportunity__title', 'talent__user__email')
