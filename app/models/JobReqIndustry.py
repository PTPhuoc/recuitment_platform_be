from django.db import models
from django_ulidfield import ULIDField

class JobReqIndustry(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    job_req = models.ForeignKey("JobReq", on_delete=models.CASCADE, related_name='industry_links', db_column='jobReqId')
    industry = models.ForeignKey("Industry", on_delete=models.CASCADE, related_name='job_req_industry_links', db_column='industryId')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'JobReqIndustry'
        unique_together = ('job_req', 'industry')
