from django.db import IntegrityError
from rest_framework import serializers
from .models import Project, Asset

class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        min_length=3,
        max_length=200,
    )

    class Meta:
        model = Project
        ordering = ['-id']
        fields = ['id', 'name', 'owner', 'created_at']
        #Specifies a list of things that we want to include in the API
        read_only_fields = ['created_at', 'owner']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"name": "Project already exists"})

class AssetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        max_length=200
    )

    class Meta:
        model = Asset
        ordering = ['-id']
        fields = ['id', 'project', 'name', 'asset_type', 'is_public']

    #Implementation of Rule 1
    def validate(self, data):
        """
        Validating if project has only one asset type 3D
        """
        #We get the type of asset and its project
        asset_type = data.get('asset_type')
        project = data.get('project')

        #Checking if the type is 3D
        if asset_type == Asset.AssetType.MODEL_3D:
            #Checking if the project already has another type 3D
            existing_3d_asset = Asset.objects.filter(
                project=project,
                asset_type=Asset.AssetType.MODEL_3D
            ).exists()

            if existing_3d_asset:
                raise serializers.ValidationError(
                    "A project can only have one asset type model 3D."
                )

        return data