from django.urls import path
from .views import (
    UserProfileView,ContactUsListCreateView, TeamMemberListView, TeamMemberDetailView, ClientListView, TalentListView,
    NewsLetterListCreateView, EventView, SingleEventView, ServiceDetailView, ServiceListView,CustomTokenObtainPairView, CustomTokenRefreshView, 
    SignOutView, SignUpView, PartnerListView, PartnerDetailView, PartnerDetailView, GetAllUsersView
)

urlpatterns = [
    #partner endpoints
    path('partner/',PartnerListView.as_view(), name = 'list-partner' ),
    path('partner/<int:pk>/',PartnerDetailView.as_view(), name = 'list-partner' ),
    #contact us
    path('contact-us/',ContactUsListCreateView.as_view(), name ='contact-us'),

    path('newsletter/', NewsLetterListCreateView.as_view(), name = 'subscribe-newsletter'),
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
    
    path('contact-us/', ContactUsListCreateView.as_view(), name='contact-us-list'),
    path('team-members/', TeamMemberListView.as_view(), name='team-member-list'),
    path('team-members/<int:pk>/', TeamMemberDetailView.as_view(), name='team-member-detail'),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('talents/', TalentListView.as_view(), name='talent-list'),
    path('users/', GetAllUsersView.as_view(), name='user-list'),
    
]
