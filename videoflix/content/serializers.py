from rest_framework import serializers
from .models import Video, Video480p, Video720p, Video1080p

class VideoSerializer(serializers.ModelSerializer):
    video_480p = serializers.StringRelatedField()
    video_720p = serializers.StringRelatedField()
    video_1080p = serializers.StringRelatedField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'thumbnail', 'group', 'new_on_videoflix', 'created_at', 'video_480p', 'video_720p', 'video_1080p']
