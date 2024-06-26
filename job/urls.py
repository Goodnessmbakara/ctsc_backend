from django.urls import path

from .views import (
    ListCreateJobOpportunity, ApprovedJobOpportunity, JobOpportunitySearch, 
    LatestJobOpportunity, CategoryCountView, SingleJobOpportunity,JobApplicationDetailView,
    JobApplicationView)

urlpatterns = [
    path('job/', ListCreateJobOpportunity.as_view(), name = 'create-job'),
    path('job/<int:pk>/', SingleJobOpportunity.as_view(), name = 'create-job'),
    path('job-categories/', CategoryCountView.as_view(), name='category-count'),
    path('job-approved/',ApprovedJobOpportunity.as_view(), name = 'approved-jobs' ),
    path('job-search/', JobOpportunitySearch.as_view(), name='job-search'),
    path('job_applications/', JobApplicationView.as_view(), name='job_applications'),
    path('job_applications/<int:pk>/', JobApplicationDetailView.as_view(), name='job_applications'),
    path('latest-job/', LatestJobOpportunity.as_view(), name = 'lates-job-offers'),
]
