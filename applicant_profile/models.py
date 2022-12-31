from django.db import models
from django_mysql.models import ListCharField
from django.conf import settings
from datetime import datetime


def upload_image_path(instance, title):
    user_name = instance.user
    today = str(datetime.today())
    return f"profile_pic/{user_name}/{today}+{title}"


def upload_path_resume(instance, title):
    user_name = instance.user
    return f"resume/{user_name}/{title}"


class ApplicantProfile(models.Model):
    """
    to do break the models into small models and use the concept of relational db.
    Store these fields like city, province as separate table.
    """
    user = models.OneToOneField(
                                settings.AUTH_USER_MODEL, null=False,
                                verbose_name='user', on_delete=models.CASCADE)
    level = models.CharField(verbose_name="Job Level", max_length=50)
    skills = ListCharField(base_field=models.CharField(max_length=50),
                           size=15,
                           max_length=(51 * 16),
                           verbose_name="Applicant Skills")
    experience = models.PositiveSmallIntegerField(verbose_name="years of experience")
    date_of_birth = models.DateField(verbose_name="date of birth")
    gender = models.CharField(verbose_name="gender", max_length=25)
    profile_pic = models.ImageField(verbose_name="profile pic", upload_to=upload_image_path, null=True)
    resume = models.FileField(verbose_name="resume", upload_to=upload_path_resume, null=True, blank=True)
    expected_salary = models.IntegerField(verbose_name="expected salary")
    street = models.CharField(verbose_name="street address", max_length=150)
    city = models.CharField(verbose_name="city", max_length=150)
    province = models.CharField(verbose_name="province", max_length=150)
    preferred_job_location = ListCharField(base_field=models.CharField(max_length=50),
                                           size=5,
                                           max_length=(6 * 51),
                                           verbose_name="preferred job location")
