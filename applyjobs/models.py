from django.db import models
from django.conf import settings

from job import models as job_model


class ApplyJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name="user id")
    job = models.ForeignKey(job_model.Job,
                            on_delete=models.CASCADE,
                            verbose_name="job id")
    date_posted = models.DateField(verbose_name="job date posted",
                                   auto_now_add=True)
    job_name = models.CharField(verbose_name="job name",
                                max_length=150)
