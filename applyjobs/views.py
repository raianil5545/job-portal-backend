from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response, status
from django.core.mail import EmailMessage

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
                if request.user.role == "applicant":
                    return request.user == obj.user
                return False
            return False
        return False


class ApplyJobViewSet(ModelViewSet):
    authentication_classes = [custom_auth.CustomUserAuthentication, ]
    permission_classes = [ApplyJobPermission, ]
    queryset = apply_job_model.ApplyJob.objects.all()
    serializer_class = apply_job_serializer.ApplyJobSerializer


    def list(self, request, *args, **kwargs):
        user = request.user
        applied_jobs = apply_job_model.ApplyJob.objects.filter(user=user)
        applied_job_list = [apply_job_serializer.ApplyJobSerializer(job).data for job in applied_jobs]
        return response.Response(applied_job_list)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = apply_job_serializer.ApplyJobSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        receiver_emails = [data.get("job").user, request.user]
        try:
            pass
            email = EmailMessage(subject="test",
                                 body='That’s your message body',
                                 from_email="jobportal@gmail.com",
                                 to=receiver_emails,
                                 bcc=['bcc@anotherbestuser.com'],
                                 reply_to=['whoever@itmaybe.com'],
                                 )
            email.send(fail_silently=False)
        except Exception as ex:
            return response.Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer.create(validated_data=data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)





