# serializers.py
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from .models import OutreachBatch, Photo, Video


def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB limit
        raise ValidationError("The maximum file size that can be uploaded is 10MB")

class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validate_file_size])

    class Meta:
        model = Photo
        fields = ['id', 'image', 'uploaded_at']

class VideoSerializer(serializers.ModelSerializer):
    video = serializers.FileField(validators=[validate_file_size])

    class Meta:
        model = Video
        fields = ['id', 'video', 'uploaded_at']

class OutreachBatchSerializer(serializers.ModelSerializer):
   photos = PhotoSerializer(many=True, required=False)
   videos = VideoSerializer(many=True, required=False)

   class Meta:
        model = OutreachBatch
        fields = ['id', 'description', 'created_at', 'updated_at', 'photos', 'videos']

class OutreachBatchCreateSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    videos = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = OutreachBatch
        fields = ['description', 'photos', 'videos']

    def validate(self, data):
        photos = data.get('photos', [])
        videos = data.get('videos', [])
        if len(photos) > 50:
            raise serializers.ValidationError("Maximum 50 photos allowed.")
        if len(videos) > 50:
            raise serializers.ValidationError("Maximum 50 videos allowed.")
        return data

    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])
        videos_data = validated_data.pop('videos', [])
        outreach_batch = OutreachBatch.objects.create(**validated_data)
        Photo.objects.bulk_create([
            Photo(outreach_batch=outreach_batch, image=photo) for photo in photos_data
        ])
        Video.objects.bulk_create([
            Video(outreach_batch=outreach_batch, video=video) for video in videos_data
        ])
        return outreach_batch