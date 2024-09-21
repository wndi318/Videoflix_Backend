from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Video
from .serializers import VideoSerializer
from django.urls import reverse
from rest_framework import status

class VideoModelTest(TestCase):

    def setUp(self):
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            video_file="videos/test_video.mp4",
            group="drama",
        )

    def test_video_creation(self):
        self.assertEqual(self.video.title, "Test Video")
        self.assertEqual(self.video.group, "drama")
        self.assertTrue(isinstance(self.video, Video))
        self.assertEqual(str(self.video), "Test Video")

class VideoAPITest(APITestCase):

    def setUp(self):
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            video_file="videos/test_video.mp4",
            group="drama",
        )
        self.url = reverse('video-list')

    def test_get_video_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Video')

    def test_video_detail(self):
        url = reverse('video-detail', kwargs={'pk': self.video.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Video')

class VideoSerializerTest(TestCase):

    def setUp(self):
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            video_file="videos/test_video.mp4",
            group="drama",
        )
        self.serializer = VideoSerializer(instance=self.video)

    def test_serializer_data(self):
        data = self.serializer.data
        self.assertEqual(data['title'], 'Test Video')
        self.assertEqual(data['group'], 'drama')