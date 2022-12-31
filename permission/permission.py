from rest_framework import permissions, exceptions


class IsOwnerOperations(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == obj.user.role:
            if view.action == 'create':
                return True
            else:
                return request.user == obj.user
        else:
            return False


