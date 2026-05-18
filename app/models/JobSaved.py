from django.db import models
from django_ulidfield import ULIDField

from app.models import Account, Job


class JobSaved(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='job_saved', db_column='accountId')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job', db_column='jobId')

    class Meta:
        db_table = 'JobSaved'