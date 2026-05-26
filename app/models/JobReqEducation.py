from django.db import models
from django_ulidfield import ULIDField

class JobReqEducation(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    job_req = models.ForeignKey("JobReq", on_delete=models.CASCADE, related_name='education_links', db_column='jobReqId')
    education = models.ForeignKey("Education", on_delete=models.CASCADE, related_name='job_req_education_links', db_column='educationId')
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'JobReqEducation'
        unique_together = ('job_req', 'education')