from django.contrib import admin
from . import models


@admin.register(models.ApplyJob)
class ApplyJobAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "job"]
