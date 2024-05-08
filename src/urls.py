from django.urls import path
from .views import (
    ContactUsView, StoryDetailView, StoryListView,PreviousFeaturedStoriesView,
    CommentCreateView,ReplyCreateView, LatestFeaturedStoryView, LikeCreateView, UserProfileView,
    NewsLetterCreateView, EventView, SingleEventView, ServiceDetailView, ServiceListView,CustomTokenObtainPairView, CustomTokenRefreshView, SignOutView, SignUpView
)

urlpatterns = [
    #contact us
    path('contact-us/',ContactUsView.as_view(), name ='contact-us'),
    path('story/feature-story/', LatestFeaturedStoryView.as_view(), name = 'weekly-featured-story'),
    path('story/previously-featured-stories/' ,PreviousFeaturedStoriesView.as_view(), name = 'all-featured-stories'),
    path('story/', StoryListView.as_view(), name = 'list-story'),
    path('story/<str:story_id>/', StoryDetailView.as_view(), name = 'detail-story'),
    path('story/<str:story_id>/comment/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:comment_id>/reply/', ReplyCreateView.as_view(), name='reply-create'),
    path('comment/<int:comment_id>/like/', LikeCreateView.as_view(), name='like-comment'),
    path('newsletter/', NewsLetterCreateView.as_view(), name = 'subscribe-newsletter'),
    #event endpoints
    path('event/<int:event_id>/', SingleEventView.as_view(), name = 'sngle-event'),
    path('event/', EventView.as_view(), name = 'list-events'),

    #service endpoints
    path('service/', ServiceListView.as_view(), name = 'list-services'),
    path('service/<int:service_id>/', ServiceDetailView.as_view(), name = 'single-service'),
    
    #auth endpoints
    path('sign-in/', CustomTokenObtainPairView.as_view(), name='sign-in'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('sign-out/', SignOutView.as_view(), name='sign_out'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    
    #user endpoints
    path('user-profile/', UserProfileView.as_view(), name='user_profile'),
]
