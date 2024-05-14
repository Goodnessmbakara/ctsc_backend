from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import (
    ContactUs,Service,Partner,TalentProfile,ClientProfile,
    Newsletter, Event, TeamMember)
from .serializers import (
    ContactUsSerializer,PartnerSerializer,ServiceDetailSerializer,
    NewsLetterSerializer, UserProfileSerializer,TalentProfileSerializer,ClientProfileSerializer,
    ServiceSerializer,SignUpSerializer, CustomTokenObtainPairSerializer,
     EventSerializer, TeamMemberSerializer)
User = get_user_model()

class TeamMemberView(APIView):
    serializer_class = TeamMemberSerializer
    def get(self,request, format=None):
        members = TeamMember.objects.all()
        serializer = self.serializer_class(data = members, many =True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class PartnerListView(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class PartnerDetailView(generics.RetrieveAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = TalentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_client:
            return ClientProfile.objects.filter(user=user)
        elif user.is_talent:
            return TalentProfile.objects.filter(user=user)
        return User.objects.filter(email = user.email)

    def get_object(self):
        return self.get_queryset().get()

    def get_serializer_class(self):
        user = self.request.user
        if user.is_client:
            return ClientProfileSerializer
        elif user.is_talent:
            return TalentProfileSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance = self.request.user
        user_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # Update profile details based on user type
        if instance.is_talent:
            profile_instance = TalentProfile.objects.get(user=instance)
            profile_serializer = TalentProfileSerializer(profile_instance, data=request.data.get('profile', {}), partial=partial)
        elif instance.is_client:
            profile_instance = ClientProfile.objects.get(user=instance)
            profile_serializer = ClientProfileSerializer(profile_instance, data=request.data.get('profile', {}), partial=partial)

        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        return Response(user_serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    pass

class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context= {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignOutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class CustomServicePagination(PageNumberPagination):
    page_size = 6
    max_page_size = 100

class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    pagination_class = CustomServicePagination

class ServiceDetailView(generics.RetrieveAPIView):
    serializer_class = ServiceDetailSerializer
    queryset = Service.objects.prefetch_related('talent_profiles')
    lookup_field = 'service_id'
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

class NewsLetterCreateView(APIView):
    serializer_class = NewsLetterSerializer
    queryset = Newsletter.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        if Newsletter.objects.filter(email_address=data['email_address']).exists():
            return Response({'message: This User is already Subscribed to our Newsletter'} ,status = status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data = data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response({'message: welcome to our newsletter. you have successfully been onboarded'} ,status = status.HTTP_201_CREATED)


