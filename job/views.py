from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response, status, exceptions

from account import authentication
from . import serializer as job_serializer
from . import models


class JobsOperations(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == "employer":
                return True
            else:
                return request.method in permissions.SAFE_METHODS
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user == obj.user
        else:
            return request.method in permissions.SAFE_METHODS


class JobViewSet(ModelViewSet):
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = [JobsOperations, ]

    queryset = models.Job.objects.all()
    serializer_class = job_serializer.JobSerializer




