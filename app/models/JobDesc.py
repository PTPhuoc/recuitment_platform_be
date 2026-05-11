from django.db import models
from django_ulidfield import ULIDField
from app.models import Job


class JobDesc(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='desc', db_column='jobId')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    index = models.IntegerField(default=0)

    class Meta:
        db_table = 'JobDesc'