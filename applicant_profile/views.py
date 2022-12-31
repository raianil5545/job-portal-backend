from rest_framework import permissions, response, status, exceptions
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from . import models

from account import authentication
from . import serializer as app_profile_serializer
from permission import permission


class ApplicantProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = [permissions.IsAuthenticated|permission.IsOwnerOperations]
    queryset = models.ApplicantProfile.objects.all()
    serializer_class = app_profile_serializer.ApplicantProfileSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role != "applicant":
            raise exceptions.PermissionDenied("Not an applicant")
        profile = get_object_or_404(models.ApplicantProfile, user=user)
        serializer = app_profile_serializer.ApplicantProfileSerializer(profile)
        return response.Response(serializer.data, status=status.HTTP_200_OK)








