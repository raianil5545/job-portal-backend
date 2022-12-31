from django.contrib import admin
from . import models


@admin.register(models.Job)
class JobModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "job_name", "job_category",
                    "job_level", "no_of_vacancy", "employment_type",
                    "street_address", "city", "offered_salary", "application_deadline",
                    "education_level", "experience_level", "skills_required"]


