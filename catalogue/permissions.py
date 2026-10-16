from rest_framework import permissions
from catalogue.models import Project

class IsAdminOrCommercial(permissions.BasePermission):
    """
    Manages what each user is allowed to see
    """
    def has_permission(self, request, view):
        #We test if the user is valid
        if not request.user or not request.user.is_authenticated:
            return False

        #Now, implementation of rule 3.
        if request.method == 'POST' and 'project' in request.data:
            project_id = request.data.get('project')
            try:
                project = Project.objects.get(id=project_id)
                if project.owner != request.user:
                    return False
            except Project.DoesNotExist:
                return False

        return True

    def has_object_permission(self, request, view, obj):
        #If the user is administrator, they have access to everything
        if request.user.is_staff or request.user.groups.filter(name='admin').exists():
            return True

        #If they are commercial, we apply rule 2 + we test if it's a project or asset
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'project'):
            return obj.project.owner == request.user

        return False