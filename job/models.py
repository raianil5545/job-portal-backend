from django.db import models
from django_mysql.models import ListCharField
from django.conf import settings
from datetime import date


class Job(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name="user")
    job_name = models.CharField(verbose_name="job  name",
                                max_length=150)
    job_category = models.CharField(verbose_name="job category",
                                    max_length=150)
    job_level = models.CharField(verbose_name="job level",
                                 max_length=150)
    no_of_vacancy = models.PositiveSmallIntegerField(verbose_name="no of vacancy")
    employment_type = models.CharField(verbose_name="employment type",
                                       max_length=150)
    street_address = models.CharField(verbose_name="street address",
                                      max_length=150)
    city = models.CharField(verbose_name="city",
                            max_length=100)
    offered_salary = models.CharField(verbose_name="offered salary",
                                      max_length=150)
    application_deadline = models.DateField(verbose_name="application deadline")
    education_level = models.CharField(verbose_name="education level",
                                       max_length=150)
    experience_level = models.CharField(verbose_name="years of experience",
                                        max_length=100)
    skills_required = ListCharField(base_field=models.CharField(max_length=100),
                                    size=10,
                                    max_length=(101*11),
                                    verbose_name="skills required")
    other_specifications = models.TextField(verbose_name="other specifications",
                                            max_length=1500)
    job_description = models.TextField(verbose_name="job description",
                                       max_length=2000)

    @property
    def time_till(self):
        today = date.today()
        days_till = self.application_deadline - today
        return days_till

    @property
    def is_job_active(self):
        days_till = self.time_till()
        if days_till > 0:
            return True
        return False


