from rest_framework.viewsets import ModelViewSet
from account.authentication import CustomUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions, response, status
from django.shortcuts import get_object_or_404
from . import models
from . import serializer as em_serializer
from permission import permission


class EmployerProfileViewSet(ModelViewSet):
    authentication_classes = (CustomUserAuthentication, )
    permission_classes = (IsAuthenticated, permission.IsOwnerOperations, )
    queryset = models.EmployerProfile.objects.all()
    serializer_class = em_serializer.EmployerProfileSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role != "employer":
            raise exceptions.PermissionDenied("Employers only")
        profile = get_object_or_404(models.EmployerProfile, user=user)
        serializer = em_serializer.EmployerProfileSerializer(profile)
        return response.Response(serializer.data, status=status.HTTP_200_OK)





