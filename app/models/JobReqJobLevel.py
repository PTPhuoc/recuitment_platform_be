from django.db import models
from django_ulidfield import ULIDField

class JobReqJobLevel(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    job_req = models.ForeignKey("JobReq", on_delete=models.CASCADE, related_name='job_level_links', db_column='jobReqId')
    job_level = models.ForeignKey("JobLevel", on_delete=models.CASCADE, related_name='job_req_level_links', db_column='jobLevelId')
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'JobReqJobLevel'
        unique_together = ('job_req', 'job_level')