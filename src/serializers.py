from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ContactUs, Story, Comment

User = get_user_model()


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('first_name', 'email_address', 'last_name', 'message')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'comment_body')

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('story_id', 'topic', 'image', 'short_description', 'created_at', 'author')

class StoryDetailSerializer(serializers.ModelSerializer):
    comment_id = CommentSerializer()
    model = Story
    fields = ('story_id', 'topic', 'image', 'short_description', 'created_at', 'author','body', 'comment_id')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'

# class SkillCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SkillCategory
#         fields = '__all__'

# class SkillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Skill
#         fields = '__all__'

# class JobOpportunitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JobOpportunity
#         fields = '__all__'

# class JobApplicationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JobApplication
#         fields = '__all__'
