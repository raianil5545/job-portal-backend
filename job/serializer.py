from rest_framework.serializers import ModelSerializer
from . import models as job_models


class JobSerializer(ModelSerializer):
    class Meta:
        model = job_models.Job
        fields = ["id", "user", "job_name", "job_category",
                  "job_level", "no_of_vacancy", "employment_type",
                  "street_address", "city", "offered_salary",
                  "application_deadline", "education_level", "experience_level",
                  "skills_required", "other_specifications", "job_description"]

        read_only_fields = ["id"]
