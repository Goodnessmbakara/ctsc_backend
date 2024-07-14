from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import JobApplication, JobOpportunity
from .serializers import (CategoryCountSerializer, JobApplicationSerializer,
                          JobSerializer)


class CategoryCountView(generics.GenericAPIView):
    serializer_class = CategoryCountSerializer
    @swagger_auto_schema(
        operation_description="Get category counts",
        responses={
            200: openapi.Response(
                description='Category counts',
                schema=CategoryCountSerializer(many=True)
            )
        }
    )

    def get(self, request, *args, **kwargs):
        categories = JobOpportunity.objects.values('category').annotate(count=Count('category')).order_by('-count')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        # This method is required for ListAPIView, but we're not using it directly
        return JobOpportunity.objects.none()

class JobApplicationView(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_class = [IsAuthenticated]
    
class JobApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_class = [IsAuthenticated]
    
class LatestJobOpportunity(generics.ListAPIView):
    queryset = JobOpportunity.objects.all().order_by('-created_at')[:3]
    serializer_class = JobSerializer

class ListCreateJobOpportunity(generics.ListCreateAPIView):
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