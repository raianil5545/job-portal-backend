from django.db import models
from django.conf import settings
from job import models as job_model


class JobPosted(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name="user id",
                             on_delete=models.CASCADE)
    job = models.ForeignKey(job_model.Job,
                            verbose_name="job id",
                            on_delete=models.CASCADE)
    date_job_posted = models.DateField(verbose_name="date on job posted")
    job_name: models.CharField(verbose_name="jon name")


