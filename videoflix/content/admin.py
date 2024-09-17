from django.contrib import admin
from .models import Video, Video480p, Video720p, Video1080p
from import_export.admin import ImportExportModelAdmin

class VideoAdmin(ImportExportModelAdmin):
    list_display = ('title', 'description', 'created_at', 'video_file',)

admin.site.register(Video, VideoAdmin)
admin.site.register(Video480p)
admin.site.register(Video720p)
admin.site.register(Video1080p)
