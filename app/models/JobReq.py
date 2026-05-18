from django.db import models
from django_ulidfield import ULIDField
from app.models import Job

class JobReq(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='req', db_column='jobId')
    form_of_job = models.CharField(max_length=100, null=True, db_column="formOfJob", default='Không yêu cầu')
    location = models.CharField(max_length=100, null=True)
    quantity = models.IntegerField(default=0)
    career = models.CharField(max_length=255, null=True, default='Không yêu cầu')
    education = models.CharField(max_length=255, null=True, default='Không yêu cầu')
    max_salary = models.IntegerField(default=0)
    min_salary = models.IntegerField(default=0)
    max_experience = models.IntegerField(default=0)
    min_experience = models.IntegerField(default=0)

    class Meta:
        db_table = 'JobReq'