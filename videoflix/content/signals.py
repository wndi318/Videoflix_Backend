import os
import django_rq
from .models import Video, Video480p, Video720p, Video1080p
from .tasks import convert_480p, convert_720p, convert_1080p, create_thumbnail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created: 
        base_filename = os.path.basename(instance.video_file.name)

        video_480p_path = os.path.join('videos', base_filename.replace(".mp4", "_480p.mp4"))
        video_720p_path = os.path.join('videos', base_filename.replace(".mp4", "_720p.mp4"))
        video_1080p_path = os.path.join('videos', base_filename.replace(".mp4", "_1080p.mp4"))
        
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_480p, instance.video_file.path)
        queue.enqueue(convert_720p, instance.video_file.path)
        queue.enqueue(convert_1080p, instance.video_file.path)
        queue.enqueue(create_thumbnail, instance.video_file.path)


        video_480p_instance = Video480p(video=instance)
        video_480p_instance.video_file_480p = video_480p_path
        video_480p_instance.save()

        video_720p_instance = Video720p(video=instance)
        video_720p_instance.video_file_720p = video_720p_path
        video_720p_instance.save()

        video_1080p_instance = Video1080p(video=instance)
        video_1080p_instance.video_file_1080p = video_1080p_path
        video_1080p_instance.save()

        thumbnail_path = os.path.join('thumbnails', base_filename.replace(".mp4", "_thumbnail.jpg"))
        instance.thumbnail.name = thumbnail_path
        instance.save()

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes video file, converted files, and thumbnail when the Video object is deleted.
    """
    if instance.video_file and os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)

    for resolution in ['_480p.mp4', '_720p.mp4', '_1080p.mp4', '_thumbnail.jpg']:
        file_path = instance.video_file.path.replace(".mp4", resolution)
        if os.path.isfile(file_path):
            os.remove(file_path)
