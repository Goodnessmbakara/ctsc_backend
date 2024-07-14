# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OutreachBatchViewSet

router = DefaultRouter()
router.register(r'outreach-batches', OutreachBatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]