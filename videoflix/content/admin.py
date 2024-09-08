from django.contrib import admin
from .models import Video, Video480p, Video720p

admin.site.register(Video)
admin.site.register(Video480p)
admin.site.register(Video720p)
