from django.db.models.query_utils import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Project, Asset
from .serializers import ProjectSerializer, AssetSerializer
from .permissions import IsAdminOrCommercial

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrCommercial]

    filter_backends = [SearchFilter]
    search_fields = ['name', 'owner__username']

    #We apply rule 2 because the one on permissions only affects individual "get"s
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name='admin').exists():
            queryset = Project.objects.all()
            print(
                f'[DEBUG] ProjectViewSet.get_queryset() with admin user access.'
                f' projects: {queryset.count()}'
            )
            return queryset
        queryset = Project.objects.filter(owner=user)
        print(f'[DEBUG] ProjectViewSet.get_queryset() with regular user access.'
              f' projects: {queryset.count()}')
        return queryset

    #I've added this one so they detect the owner automatically
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsAdminOrCommercial]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['asset_type']
    search_fields = ['name', 'project__owner__username']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name='admin').exists():
            queryset = Asset.objects.all()
            print(
                f'[DEBUG] AssetViewSet.get_queryset() with admin user access.'
                f' assets: {queryset.count()}'
            )
            return queryset
        #This is to show the ones with "is_public" as True by adding them with an or,
        #and preventing duplicates with distinct
        queryset = Asset.objects.filter(Q(project__owner=user) | Q(is_public=True)).distinct()
        print(
            f'[DEBUG] AssetViewSet.get_queryset() with regular user access.'
            f' assets: {queryset.count()}'
        )
        return queryset