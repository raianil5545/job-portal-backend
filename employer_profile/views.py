from rest_framework.viewsets import ModelViewSet
from account.authentication import CustomUserAuthentication
from rest_framework import exceptions, response, status
from django.shortcuts import get_object_or_404
from . import models
from . import serializer as em_serializer
from rest_framework import permissions


class EmployerProfileOperationsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            if request.user.is_authenticated:
                if request.user.role == "employer":
                    return True
                return False
            return False
        return False

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_authenticated:
                return request.user == obj.user
            return False
        return False


class EmployerProfileViewSet(ModelViewSet):
    authentication_classes = (CustomUserAuthentication, )
    permission_classes = (EmployerProfileOperationsPermission, )
    queryset = models.EmployerProfile.objects.all()
    serializer_class = em_serializer.EmployerProfileSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role != "employer":
            raise exceptions.PermissionDenied("Employers only")
        profile = get_object_or_404(models.EmployerProfile, user=user)
        serializer = em_serializer.EmployerProfileSerializer(profile)
        return response.Response(serializer.data, status=status.HTTP_200_OK)







