from rest_framework import serializers
from applicant_profile import models as applicant_model


class ApplicantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = applicant_model.ApplicantProfile
        fields = ["id", "user", "level", "skills", "experience", "date_of_birth",
                  "gender", "profile_pic", "expected_salary", "street", "city",
                  "province", "preferred_job_location", "resume"]

        read_only_fields = ["id"]
