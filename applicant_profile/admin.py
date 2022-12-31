from django.contrib import admin
from . import models


@admin.register(models.ApplicantProfile)
class AccountAminModel(admin.ModelAdmin):
    list_display = ["id", "level", "user", "skills", "experience",
                    "date_of_birth", "gender", "profile_pic", "resume",
                    "expected_salary", "street", "city", "province",
                    "preferred_job_location"]
