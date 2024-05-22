from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Like, Comment, Story

from django.contrib.auth import get_user_model
from rest_framework import serializers

from src.serializers import UserSerializer
User =get_user_model()
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        likes = Like.objects.filter(pk = obj.id)
        return likes.count()

    def get_replies(self, obj):
        replies = Comment.objects.filter(reply_to=obj)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data
    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment_body', 'replies', 'likes_count']


class StorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    author = UserSerializer()

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
    class Meta:
        model = Story
        fields = ('story_id', 'topic', 'image', 'short_description', 'created_at', 'author')

class StoryDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Story
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
