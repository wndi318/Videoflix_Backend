from rest_framework import serializers
from django.conf import settings
from .models import Video, Video480p, Video720p, Video1080p

class VideoSerializer(serializers.ModelSerializer):
    video_480p = serializers.StringRelatedField()
    video_720p = serializers.StringRelatedField()
    video_1080p = serializers.StringRelatedField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'thumbnail_url', 'group', 'new_on_videoflix', 'created_at', 'video_480p', 'video_720p', 'video_1080p']

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None
