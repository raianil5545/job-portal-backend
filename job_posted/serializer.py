from rest_framework import serializers
from . import models as job_posted_models


class JobPostedSerializer(serializers.ModelSerializer):
    class Meta:
        model = job_posted_models.JobPosted
        fields = ["id", "user", "job", "date_job_posted", "job_name"]
        read_only_fields = ["id"]
