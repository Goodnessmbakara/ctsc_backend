from rest_framework import serializers

from .models import JobApplication, JobOpportunity

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpportunity
        exclude = ('is_approved',)
        read_only_fields = ['is_approved']