from django.urls import path

from .views import (StoryDetailView, StoryListView,
                    PreviousFeaturedStoriesView,CreateListAnonymousStoryView,
    CommentCreateView,ReplyCreateView, LatestFeaturedStoryView, LikeCreateView)


urlpatterns = [
    path('anonymous-story/', CreateListAnonymousStoryView.as_view(), name = 'anonymous-story'),
    path('story/feature-story/', LatestFeaturedStoryView.as_view(), name = 'weekly-featured-story'),
    path('story/previously-featured-stories/' ,PreviousFeaturedStoriesView.as_view(), name = 'all-featured-stories'),
    path('story/', StoryListView.as_view(), name = 'list-story'),
    path('story/<str:story_id>/', StoryDetailView.as_view(), name = 'detail-story'),
    path('story/<str:story_id>/comment/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:comment_id>/reply/', ReplyCreateView.as_view(), name='reply-create'),
    path('comment/<int:comment_id>/like/', LikeCreateView.as_view(), name='like-comment'),
]
