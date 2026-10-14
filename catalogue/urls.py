from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, AssetViewSet

router = DefaultRouter()
router.register('project', ProjectViewSet)
router.register('asset', AssetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]