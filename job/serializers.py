from rest_framework import serializers

from .models import JobApplication, JobOpportunity
from src.models import TalentProfile
from src.serializers import TalentProfileSerializer

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpportunity
        exclude = ('is_approved',)
        read_only_fields = ['is_approved']

class JobApplicationSerializer(serializers.ModelSerializer):
    talent = TalentProfileSerializer(required = False)
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['talent', 'applied_date']
        
    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_talent:
            raise serializers.ValidationError("You need to have a talent account to be able to apply for roles")
        talent_profile = user.talent_profile
        job_application = JobApplication.objects.create(**validated_data, talent=talent_profile)
        return job_application
    
class CategoryCountSerializer(serializers.Serializer):
    category = serializers.CharField()
    count = serializers.IntegerField()