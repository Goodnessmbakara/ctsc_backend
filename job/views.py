from django.shortcuts import render

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from   rest_framework import status
from django.db.models import Count

from .models import JobApplication, JobOpportunity

from .serializers import JobSerializer, CategoryCountSerializer, JobApplicationSerializer

class CategoryCountView(generics.GenericAPIView):
    serializer_class = CategoryCountSerializer

    def get(self, request, *args, **kwargs):
        categories = JobOpportunity.objects.values('category').annotate(count=Count('category')).order_by('-count')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

class JobApplicationView(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_class = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save()
        return Response({'message': 'Application submitted successfully'}, status=status.HTTP_201_CREATED)
    
class LatestJobOpportunity(generics.ListAPIView):
    queryset = JobOpportunity.objects.all().order_by('-created_at')[:3]
    serializer_class = JobSerializer

class CreateJobOpportunity(generics.CreateAPIView):
    queryset = JobOpportunity.objects.all()
    serializer_class = JobSerializer

class SingleJobOpportunity(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobOpportunity.objects.all()
    serializer_class = JobSerializer
    
class ApprovedJobOpportunity(generics.ListAPIView):
    queryset = JobOpportunity.objects.all()
    serializer_class = JobSerializer
    def get_queryset(self):
        return JobOpportunity.objects.filter(is_approved=True)

class JobOpportunitySearch(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = JobOpportunity.objects.filter(is_approved=True)
        category = self.request.query_params.get('category')
        title = self.request.query_params.get('title')
        hiring_company = self.request.query_params.get('hiring_company')
        tag = self.request.query_params.get('tag')

        if category:
            queryset = queryset.filter(category__icontains=category)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if hiring_company:
            queryset = queryset.filter(hiring_company__icontains=hiring_company)
        if tag:
            queryset = queryset.filter(tag=tag)

        return queryset