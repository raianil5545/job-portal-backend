from rest_framework.serializers import ModelSerializer
from . import models


class EmployerProfileSerializer(ModelSerializer):
    class Meta:
        model = models.EmployerProfile
        fields = ["id", "user", "founded_year", "website_url",
                  "logo", "street_address", "city", "province",
                  "locations", "cover_page"]
        read_only_fields = ["id"]
