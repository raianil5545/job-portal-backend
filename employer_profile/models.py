from django.db import models
from django.conf import settings
from datetime import datetime
from django_mysql.models import ListCharField
from constant.constant import PROVINCE_CHOICE


def upload_logo_path(instance, title):
    user_name = instance.user
    today = datetime.today()
    return f"upload_logo/{user_name}/{today}" + title


def upload_cover_pic(instance, title):
    username = instance.user
    today = datetime.today()
    return f"upload_cover_pic/{username}/{today}" + title


class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name="user id",
                                null=False,
                                blank=False)
    founded_year = models.DateField(verbose_name="company founded date")
    website_url = models.CharField(verbose_name="company website url",
                                   max_length=250)
    logo = models.ImageField(verbose_name="company logo",
                             upload_to=upload_logo_path)
    street_address = models.CharField(verbose_name="company location street name",
                                      max_length=150)
    city = models.CharField(verbose_name="company city",
                            max_length=100)
    province = models.CharField(verbose_name="province",
                                max_length=100,
                                choices=PROVINCE_CHOICE)
    locations = ListCharField(base_field=models.CharField(max_length=100),
                              size=10,
                              max_length=(11 * 101),
                              verbose_name="company office locations")
    cover_page = models.ImageField(verbose_name="company cover pic",
                                   upload_to=upload_cover_pic)
