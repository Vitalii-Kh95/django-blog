from django.contrib.auth import get_user_model
import tempfile
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Post


class PostApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_get_blogpost(self):
        # user = get_user_model().objects.first()
        url = reverse_lazy("blogapi:posts-list")
        # img_url = "images/photo_2024-05-22_17-05-32.jpg"
        try:
            image_file = tempfile.NamedTemporaryFile(suffix=".jpg")
            image_file.write(
                b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
            )
            data = {
                "title": "test title",
                "slug": "test-title",
                "description": "description",
                "content": "content",
                "image": image_file,
                "author": "admin",
                "tags": "one",
            }
            response = self.client.post(url, data, content_type="multipart/form-data")
        finally:
            image_file.close()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, "test title")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["title"], "test title")
        self.assertEqual(response.data[0]["slug"], "test-title")
