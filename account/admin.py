from django.contrib import admin
from . import models


@admin.register(models.User)
class AccountAminModel(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "mobile_number",
        "role"
    )
