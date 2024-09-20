from rest_framework import serializers
from django.conf import settings
from .models import Video, Video480p, Video720p, Video1080p

class VideoSerializer(serializers.ModelSerializer):
    video_480p_url = serializers.SerializerMethodField()
    video_720p_url = serializers.SerializerMethodField()
    video_1080p_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'description',
            'video_file',
            'thumbnail_url',
            'group',
            'new_on_videoflix',
            'created_at',
            'video_480p_url',
            'video_720p_url',
            'video_1080p_url'
        ]

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if request and obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None

    def get_video_480p_url(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'video_480p') and obj.video_480p and obj.video_480p.video_file_480p:
            return request.build_absolute_uri(obj.video_480p.video_file_480p.url)
        return None

    def get_video_720p_url(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'video_720p') and obj.video_720p and obj.video_720p.video_file_720p:
            return request.build_absolute_uri(obj.video_720p.video_file_720p.url)
        return None

    def get_video_1080p_url(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'video_1080p') and obj.video_1080p and obj.video_1080p.video_file_1080p:
            return request.build_absolute_uri(obj.video_1080p.video_file_1080p.url)
        return None
