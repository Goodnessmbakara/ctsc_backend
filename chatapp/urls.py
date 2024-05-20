from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

router = DefaultRouter()
router.register('messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    # other URL patterns...
]