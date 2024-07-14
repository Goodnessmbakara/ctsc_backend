# views.py
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser

from .models import OutreachBatch
from .serializers import OutreachBatchCreateSerializer, OutreachBatchSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class OutreachBatchViewSet(viewsets.ModelViewSet):
    queryset = OutreachBatch.objects.prefetch_related('photos', 'videos')
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at', 'updated_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return OutreachBatchCreateSerializer
        return OutreachBatchSerializer

    @swagger_auto_schema(
        responses={
            200: OutreachBatchSerializer(many=True)
        }
    )
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=OutreachBatchCreateSerializer,
        responses={
            201: OutreachBatchSerializer
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)