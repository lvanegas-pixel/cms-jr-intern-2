from django.contrib.auth.models import User
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200) #Minimum length must be added on serializers
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE, #When user deleted, all projects deleted as well
        related_name='projects' #You can access all projects of a user with: user.projets.all()
    )
    created_at = models.DateTimeField(auto_now_add=True) #Automathic date

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='unique_name_per_owner'),
        ]

    def __str__(self):
        return self.name

class Asset(models.Model):
    class AssetType(models.TextChoices): #The choices os Assets Types that we have
        MODEL_3D = 'MODEL_3D'
        IMAGE = 'IMAGE'
        VIDEO = 'VIDEO'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='assets'
    )
    name = models.CharField(max_length=200)
    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
    )
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.asset_type})"