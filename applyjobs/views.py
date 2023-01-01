from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from . import models as apply_job_model
from . import serializers as apply_job_serializer
from account import authentication as custom_auth


class ApplyJobPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            if request.user.is_authenticated:
                if request.user.role == "applicant":
                    return True
            return False
        return False

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_authenticated:
                return request.user.role == object.user.role
            return False
        return False


class ApplyJobViewSet(ModelViewSet):
    authentication_classes = [custom_auth.CustomUserAuthentication, ]
    permission_classes = [ApplyJobPermission, ]
    queryset = apply_job_model.ApplyJob.objects.all()
    serializer_class = apply_job_serializer.ApplyJobSerializer
