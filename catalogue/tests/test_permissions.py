from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from catalogue.models import Project, Asset

class HasObjectPermissionsValidationTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.project1 = Project.objects.create(name='User 1 private project', owner=self.user1)
        self.project2 = Project.objects.create(name='User 2 private project', owner=self.user2)
        self.asset1 = Asset.objects.create(
            project=self.project1,
            name='User 1 private asset',
            asset_type='VIDEO',
            is_public=False
        )
        self.asset2 = Asset.objects.create(
            project=self.project2,
            name='User 2 private asset',
            asset_type='VIDEO',
            is_public=False
        )
        self.asset3 = Asset.objects.create(
            project=self.project2,
            name='User 2 public asset',
            asset_type='VIDEO',
            is_public=True
        )

    def test_commercial_user_cant_see_private_projects(self):
        self.client.force_authenticate(user=self.user2)

        url = f'/api/projects/{self.project1.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_commercial_user_cant_see_private_assets(self):
        self.client.force_authenticate(user=self.user2)

        url = f'/api/assets/{self.asset1.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_commercial_user_can_see_theirs_and_public_assets(self):
        self.client.force_authenticate(user=self.user1)

        url = '/api/assets/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        asset_names = [asset['name'] for asset in response.data]
        self.assertIn('User 2 public asset', asset_names)
        self.assertIn('User 1 private asset', asset_names)
        self.assertNotIn('User 2 private asset', asset_names)


class HasPermissionsValidationTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_superuser(username='user2', password='password123')

        self.project1 = Project.objects.create(name='User 1 private project', owner=self.user1)

        self.url = '/api/projects/'

    def test_impossible_to_create_an_asset_for_others_private_projects(self):
        self.client.force_authenticate(user=self.user2)

        invalid_data = {
            'project': self.project1.id,
            'name': 'Invalid asset',
            'asset_type': Asset.AssetType.MODEL_3D,
            'is_public': False,
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_impossible_to_create_an_asset_for_unexisting_projects(self):
        self.client.force_authenticate(user=self.user1)

        invalid_data = {
            'project': 1083,
            'name': 'Invalid asset',
            'asset_type': Asset.AssetType.MODEL_3D,
            'is_public': False,
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)