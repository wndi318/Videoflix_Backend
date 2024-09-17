from django.db import models
from datetime import date

class Video(models.Model):
    GROUP_CHOICES = (
        ('documentary', 'Documentary'),
        ('drama', 'Drama'),
        ('romance', 'Romance'),
    )
    
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.FileField(upload_to='thumbnails', blank=True, null=True)
    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default="documentary")
    new_on_videoflix = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Video480p(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='video_480p')
    video_file_480p = models.FileField(upload_to="videos", blank=True, null=True)
    
    def __str__(self):
        return f"{self.video.title}_480p"
    

class Video720p(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='video_720p')
    video_file_720p = models.FileField(upload_to="videos", blank=True, null=True)
    
    def __str__(self):
        return f"{self.video.title}_720p"

class Video1080p(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='video_1080p')
    video_file_1080p = models.FileField(upload_to="videos", blank=True, null=True)
    
    def __str__(self):
        return f"{self.video.title}_1080p"