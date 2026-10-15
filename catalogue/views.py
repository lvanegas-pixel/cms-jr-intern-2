from django.db.models.query_utils import Q
from rest_framework import viewsets
from .models import Project, Asset
from .serializers import ProjectSerializer, AssetSerializer
from .permissions import IsAdminOrCommercial

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrCommercial]

    #We apply rule 2 because the one on permissions only affects individual "get"s
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name='admin').exists():
            return Project.objects.all()
        return Project.objects.filter(owner=user)

    #I've added this one so they detect the owner automatically
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsAdminOrCommercial]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name='admin').exists():
            return Asset.objects.all()
        #I've added in this part the ones with "is_public" as True by adding them with an or,
        #and preventing duplicates with distinct
        return Asset.objects.filter(Q(project__owner=user) | Q(is_public=True)).distinct()