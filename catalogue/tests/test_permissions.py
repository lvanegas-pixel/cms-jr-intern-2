from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from catalogue.models import Project, Asset

class HasObjectPermissionsValidationTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.project1 = Project.objects.create(name='User 1 project', owner=self.user1)
        self.project2 = Project.objects.create(name='User 2 project', owner=self.user2)

        self.asset_user1 = Asset.objects.create(
            project=self.project1,
            name='User 1 private asset',
            asset_type='VIDEO',
            is_public=False
        )
        self.asset_user2 = Asset.objects.create(
            project=self.project2,
            name='User 2 private asset',
            asset_type='VIDEO',
            is_public=False
        )
        self.asset_public = Asset.objects.create(
            project=self.project2,
            name='Public asset',
            asset_type='IMAGE',
            is_public=True
        )

    def test_commercial_user_can_see_only_their_projects(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifying there's only one project and it's his
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'User 1 project')

    def test_commercial_user_can_see_their_assets_and_the_public_assets(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get('/api/assets/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        asset_names = [asset['name'] for asset in response.data]
        self.assertIn('Public asset', asset_names)
        self.assertIn('User 1 private asset', asset_names)
        self.assertNotIn('User 2 private asset', asset_names)

    def test_admin_user_can_see_everything(self):
        admin_user = User.objects.create_superuser(username='admin', password='password123')
        self.client.force_authenticate(user=admin_user)

        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)