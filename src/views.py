from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ContactUs,Story,Comment, Like, Newsletter, Event
from .serializers import (ContactUsSerializer, StoryDetailSerializer,
                          StorySerializer,NewsLetterSerializer,
                          CommentSerializer, LikeSerializer, EventSerializer)
User = get_user_model()


class EventView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SingleEventView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'event_id'

class ContactUsView(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class =  ContactUsSerializer

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        story_id = self.kwargs.get('story_id')
        story = get_object_or_404(Story,story_id = story_id)
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None, story=story)

class ReplyCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        comment_id = self.kwargs.get('comment_id')
        parent_comment = get_object_or_404(Comment, pk=comment_id)
        serializer.save(
            user=self.request.user if self.request.user.is_authenticated else None,
            reply_to=parent_comment, story_id =parent_comment.story_id
        )


class StoryListView(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class =  StorySerializer

class StoryDetailView(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class =  StoryDetailSerializer
    lookup_field = 'story_id'


class LatestFeaturedStoryView(APIView):
    def get(self, request, *args, **kwargs):
        latest_featured_story = Story.get_latest_featured_story()
        if latest_featured_story:
            serializer = StorySerializer([latest_featured_story], many=True)  # Convert single object to list
            return Response(serializer.data)
        else:
            return Response({"message": "No featured story found."}, status=status.HTTP_404_NOT_FOUND)

class PreviousFeaturedStoriesView(generics.ListAPIView):
    def get_queryset(self):
        return Story.get_previous_featured_stories()
    serializer_class = StorySerializer

class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment = Comment.objects.get(pk=comment_id)
        like, created = Like.objects.get_or_create(comment=comment, user=request.user if request.user.is_authenticated else None)
        if not created:
            return Response({"message": "You have already liked this comment."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class NewsLetterCreateView(APIView):
    serializer_class = NewsLetterSerializer
    queryset = Newsletter.objects.all()
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data = data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response({'message: welcome to our newsletter. you have successfully been onboarded'} ,status = status.HTTP_201_CREATED)


