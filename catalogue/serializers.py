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
        fields = ['id', 'name', 'owner', 'created_at']
        #Specifies a list of things that we want to include in the API
        read_only_fields = ['created_at']

class AssetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        max_length=200
    )

    class Meta:
        model = Asset
        fields = ['id', 'project', 'name', 'asset_type', 'is_public']