from django.urls import path

from .views import (StoryDetailView, StoryListView,PersonalGrowthStoryView, CulturalStoryView,InterviewStoryView,
                    PreviousFeaturedStoriesView,CreateListAnonymousStoryView,
    CommentCreateView,ReplyCreateView, LatestFeaturedStoryView, LikeCreateView, NewsStoriesView)


urlpatterns = [
    path('news_stories/',NewsStoriesView.as_view(), name = 'news-and-stories'),
    path('story/culture/', CulturalStoryView.as_view(), name  = 'cultural-story'),
    path('story/personal-growth/', PersonalGrowthStoryView.as_view(), name  = 'personal-story'),
    path('story/interview/', InterviewStoryView.as_view(), name  = 'interview-story'),
    path('anonymous-story/', CreateListAnonymousStoryView.as_view(), name = 'anonymous-story'),
    path('story/feature-story/', LatestFeaturedStoryView.as_view(), name = 'weekly-featured-story'),
    path('story/previously-featured-stories/' ,PreviousFeaturedStoriesView.as_view(), name = 'all-featured-stories'),
    path('story/', StoryListView.as_view(), name = 'list-story'),
    path('story/<str:story_id>/', StoryDetailView.as_view(), name = 'detail-story'),
    path('story/<str:story_id>/comment/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:comment_id>/reply/', ReplyCreateView.as_view(), name='reply-create'),
    path('comment/<int:comment_id>/like/', LikeCreateView.as_view(), name='like-comment'),
]

# news_stories/: returns currently featured story, two previously featured story, two personal growth story, two anonymous story,two interview story