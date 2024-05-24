from django.urls import path

from .views import CreateJobOpportunity, ApprovedJobOpportunity, JobOpportunitySearch, LatestJobOpportunity, CategoryCountView

urlpatterns = [
    path('job/', CreateJobOpportunity.as_view(), name = 'create-job'),
    path('job-categories/', CategoryCountView.as_view(), name='category-count'),
    path('job-approved/',ApprovedJobOpportunity.as_view(), name = 'approved-jobs' ),
    path('job-search/', JobOpportunitySearch.as_view(), name='job-search'),
    path('latest-job/', LatestJobOpportunity.as_view(), name = 'lates-job-offers'),
]
