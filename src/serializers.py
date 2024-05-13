from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (ContactUs,  Event,Partner, TalentProfile,
                     Newsletter, Service)

User = get_user_model()

class PartnerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)
    class Meta:
        model = Partner
        fields = ('id', 'image', 'description')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TalentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    profile_picture = serializers.SerializerMethodField()
    cv_document = serializers.SerializerMethodField()
    
    def get_profile_picture(self, obj):
        return self.context['request'].build_absolute_uri(obj.profile_picture.url)
    
    def get_cv_document(self, obj):
        return self.context['request'].build_absolute_uri(obj.cv_document.url)
    class Meta:
        model = TalentProfile
        fields = ['user', 'address', 'phone_number','profile_picture', 'cv_document', 'work_experiences']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentProfile
        fields = ['id', 'first_name', 'last_name', 'address', 'phone_number', 'is_client', 'profile_picture']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'is_client', 'is_talent']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_client=validated_data.get('is_client', False),
            is_talent=validated_data.get('is_talent', False)
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_id', 'service_name']

class ServiceDetailSerializer(serializers.ModelSerializer):
    talent_profiles = TalentProfileSerializer(many=True)
    class Meta:
        model = Service
        fields = ['service_id', 'service_name', 'talent_profiles']
class EventSerializer(serializers.ModelSerializer):

    event_image = serializers.SerializerMethodField()

    def get_event_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.event_image.url)
    class Meta:
        model = Event
        fields = '__all__'

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('first_name', 'email_address', 'last_name', 'message')

class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('first_name', 'last_name', 'email_address')
