from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from catalogue.models import Project, Asset

class HasObjectPermissionsValidationTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.project1 = Project.objects.create(name='User 1 private project', owner=self.user1)
        self.asset1 = Asset.objects.create(
            project=self.project1,
            name='User 1 private asset',
            asset_type='VIDEO',
            is_public=False
        )

    def test_commercial_user_cant_see_private_projects(self):
        self.client.force_authenticate(user=self.user2)

        url = f'/api/projects/{self.project1.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_commercial_user_cant_see_private_assets(self):
        self.client.force_authenticate(user=self.user2)

        url = f'/api/assets/{self.asset1.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HasPermissionsValidationTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_(self):
        self.assertEqual(Project.objects.count(), 0)