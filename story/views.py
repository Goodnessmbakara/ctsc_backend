from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

from .models import Comment, Like, Story

from .serializers import (StoryDetailSerializer,StorySerializer,CommentSerializer, LikeSerializer,)


class PersonalGrowthStoryView(generics.ListAPIView):
    queryset = Story.objects.filter(is_approved = True, is_anonymous = False, tags = 'Personal Growth')
    serializer_class = StorySerializer

class CulturalStoryView(generics.ListAPIView):
    queryset = Story.objects.filter(is_approved = True, is_anonymous = False, tags = 'Culture')
    serializer_class = StorySerializer

class InterviewStoryView(generics.ListAPIView):
    queryset = Story.objects.filter(is_approved = True, is_anonymous = False, tags = 'Interview')
    serializer_class = StorySerializer
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

class StoryListView(generics.ListCreateAPIView):
    queryset = Story.objects.filter(is_approved = True, is_anonymous=False)
    serializer_class =  StorySerializer

class CreateListAnonymousStoryView(APIView):
    serializer_class = StorySerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save(is_anonymous=True, is_approved=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        anonymous_stories = Story.objects.filter(is_approved=True, is_anonymous=True)
        serializer = self.serializer_class(anonymous_stories, many=True, context={'request': self.request})
        return Response(serializer.data, status =status.HTTP_200_OK)



class StoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class =  StoryDetailSerializer
    lookup_field = 'story_id'


class LatestFeaturedStoryView(APIView):
    def get(self, request, *args, **kwargs):
        latest_featured_story = Story.get_latest_featured_story()
        context = {'request':request}
        if latest_featured_story:
            serializer = StorySerializer([latest_featured_story], many=True, context=context)  # Convert single object to list
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

class NewsStoriesView(generics.GenericAPIView):
    serializer_class = StorySerializer
    @swagger_auto_schema(
        operation_description="Get news stories",
        responses={200: openapi.Response('News stories', schema=StorySerializer(many=True))}
    )
    
    def get_queryset(self):
        # This method is required for ListAPIView, but we're not using it directly
        return Story.objects.none()
    def get(self, request, *args, **kwargs):
        context = {'request': request}
        currently_featured = Story.get_latest_featured_story()
        personal_growth_stories = Story.objects.filter(is_approved=True, is_anonymous=False, tags='Personal Growth')[:2]
        anonymous_stories = Story.objects.filter(is_approved=True, is_anonymous=True)[:2]
        interview_stories = Story.objects.filter(is_approved=True, is_anonymous=False, tags='Interview')[:2]

        data = {
            'currently_featured': self.serializer_class(currently_featured, context = context).data if currently_featured else None,
            'personal_growth_stories': self.serializer_class(personal_growth_stories, many=True, context = context).data,
            'anonymous_stories': self.serializer_class(anonymous_stories, many=True, context = context).data,
            'interview_stories': self.serializer_class(interview_stories, many=True, context = context).data,
        }
        
        return Response(data)
