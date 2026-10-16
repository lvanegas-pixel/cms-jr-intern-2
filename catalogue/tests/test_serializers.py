from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from catalogue.models import Project, Asset

class AssetSerializerValidationTest(APITestCase):

    def setUp(self):
        # We create a user and a project
        self.user = User.objects.create_user(username='testuser', password='passwordtest')
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(name='Test project', owner=self.user)

        self.url = '/api/assets/'

    def test_cannot_create_multiple_3d_assets_in_same_project(self):
        # We create the first 3D model for the project
        Asset.objects.create(
            project=self.project,
            name='First 3D model',
            asset_type=Asset.AssetType.MODEL_3D,
            is_public=False
        )

        # We try creating a second 3D model
        invalid_data = {
            'project': self.project.id,
            'name': 'Second 3D model',
            'asset_type': Asset.AssetType.MODEL_3D,
            'is_public': False
        }

        # We make a POST petition
        response = self.client.post(self.url, invalid_data, format='json')

        # We verify that the code of http state is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Checking if the error message is correct
        self.assertIn("A project can only have one asset type model 3D.", str(response.data))

    def test_can_create_other_asset_types_alongside_3d(self):
        Asset.objects.create(
            project=self.project,
            name='3D model',
            asset_type=Asset.AssetType.MODEL_3D,
            is_public=False
        )

        valid_data = {
            'project': self.project.id,
            'name': 'Image',
            'asset_type': 'IMAGE',
            'is_public': True
        }

        response = self.client.post(self.url, valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)