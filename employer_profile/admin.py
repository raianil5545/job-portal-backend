from django.contrib import admin
from . import models


@admin.register(models.EmployerProfile)
class EmployeProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "founded_year", "website_url",
                    "logo", "street_address", "city", "province",
                    "locations", "cover_page"]
