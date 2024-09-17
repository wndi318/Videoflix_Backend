from django.conf import settings
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Video
from .serializers import VideoSerializer
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)

class VideoListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, format=None):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

class VideoDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, pk, format=None):
        try:
            video = Video.objects.get(pk=pk)
            serializer = VideoSerializer(video)
            return Response(serializer.data)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)