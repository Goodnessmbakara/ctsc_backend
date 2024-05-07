from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ContactUs,Story,Comment
from .serializers import (ContactUsSerializer, StoryDetailSerializer,StorySerializer,
                          CommentSerializer)
User = get_user_model()


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

# class UserCreateView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class ProfileCreateView(generics.CreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

# class SkillCategoryListView(generics.ListCreateAPIView):
#     queryset = SkillCategory.objects.all()
#     serializer_class = SkillCategorySerializer

# class SkillListView(generics.ListCreateAPIView):
#     queryset = Skill.objects.all()
#     serializer_class = SkillSerializer

# class JobOpportunityListView(generics.ListCreateAPIView):
#     queryset = JobOpportunity.objects.all()
#     serializer_class = JobOpportunitySerializer

# class JobApplicationCreateView(generics.CreateAPIView):
#     queryset = JobApplication.objects.all()
#     serializer_class = JobApplicationSerializer

# from rest_framework import generics
# from .models import Author, Topic, Story, Interview, Comment, FeaturedStory, Newsletter, Event
# from .serializers import AuthorSerializer, TopicSerializer, StorySerializer, InterviewSerializer, CommentSerializer, FeaturedStorySerializer, NewsletterSerializer, EventSerializer

# class AuthorListView(generics.ListCreateAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer

# class TopicListView(generics.ListCreateAPIView):
#     queryset = Topic.objects.all()
#     serializer_class = TopicSerializer

# class StoryListView(generics.ListCreateAPIView):
#     queryset = Story.objects.all()
#     serializer_class = StorySerializer

# class InterviewListView(generics.ListCreateAPIView):
#     queryset = Interview.objects.all()
#     serializer_class = InterviewSerializer

# class CommentListView(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

# class FeaturedStoryListView(generics.ListCreateAPIView):
#     queryset = FeaturedStory.objects.all()
#     serializer_class = FeaturedStorySerializer

# class NewsletterListView(generics.ListCreateAPIView):
#     queryset = Newsletter.objects.all()
#     serializer_class = NewsletterSerializer

# class EventListView(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer

# from rest_framework import generics
# from .models import Category
# from .serializers import CategorySerializer

# class CategoryListView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
