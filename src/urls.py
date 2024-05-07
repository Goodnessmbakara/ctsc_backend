from django.urls import path
from .views import (
    ContactUsView, StoryDetailView, StoryListView,CommentCreateView,ReplyCreateView
)

urlpatterns = [
    #contact us
    path('contact-us/',ContactUsView.as_view(), name ='contact-us'),
    path('story/', StoryListView.as_view(), name = 'list-story'),
    path('story/<str:story_id>/', StoryDetailView.as_view(), name = 'detail-story'),
    path('story/<str:story_id>/comment/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:comment_id>/reply/', ReplyCreateView.as_view(), name='reply-create'),
    # User authentication and profile creation
    # path('api/users/register/', UserCreateView.as_view(), name='user_register'),
    # path('api/users/profile/create/', ProfileCreateView.as_view(), name='user_profile_create'),

    # # Skill and category management
    # path('api/skills/', SkillListView.as_view(), name='skill_list'),
    # path('api/categories/', CategoryListView.as_view(), name='category_list'),

    # # Job opportunities
    # path('api/jobs/', JobOpportunityListView.as_view(), name='job_opportunity_list'),

    # # Other models
    # path('api/authors/', AuthorListView.as_view(), name='author_list'),
    # path('api/topics/', TopicListView.as_view(), name='topic_list'),
    # path('api/stories/', StoryListView.as_view(), name='story_list'),
    # path('api/interviews/', InterviewListView.as_view(), name='interview_list'),
    # path('api/comments/', CommentListView.as_view(), name='comment_list'),
    # path('api/featured-stories/', FeaturedStoryListView.as_view(), name='featured_story_list'),
    # path('api/newsletters/', NewsletterListView.as_view(), name='newsletter_list'),
    # path('api/events/', EventListView.as_view(), name='event_list'),
]
