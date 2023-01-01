from rest_framework.serializers import ModelSerializer
from .models import ApplyJob


class ApplyJobSerializer(ModelSerializer):
    class Meta:
        model = ApplyJob
        fields = ["id", "user", "job", "date_posted", "job_name"]
        read_only_fields = ["id", "date_posted"]
