from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response, status
from django.shortcuts import get_object_or_404

from account import authentication
from . import serializer as job_serializer
from . import models


class JobsOperations(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            if request.user.is_authenticated:
                if request.user.role == "employer":
                    return True
                else:
                    return request.method in permissions.SAFE_METHODS
            return request.method in permissions.SAFE_METHODS
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_authenticated:
                if request.method in permissions.SAFE_METHODS:
                    return True
                return request.user == obj.user
            else:
                return request.method in permissions.SAFE_METHODS
        return request.method in permissions.SAFE_METHODS


class JobViewSet(ModelViewSet):
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = [JobsOperations, ]

    queryset = models.Job.objects.all()
    serializer_class = job_serializer.JobSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        job = get_object_or_404(models.Job, pk=pk)
        serializer = job_serializer.JobSerializer(job)
        data = serializer.data
        data["time_till"] = job.time_till
        data["is_active"] = job.is_job_active
        return response.Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        jobs = models.Job.objects.all()
        jobs_data = []
        for job in jobs:
            serializer = job_serializer.JobSerializer(job)
            data = serializer.data
            data["time_till"] = job.time_till
            data["is_active"] = job.is_job_active
            jobs_data.append(data)
        return response.Response(jobs_data, status=status.HTTP_200_OK)




