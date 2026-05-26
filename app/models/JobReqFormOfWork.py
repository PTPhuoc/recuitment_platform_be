from django.db import models
from django_ulidfield import ULIDField

class JobReqFormOfWork(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    job_req = models.ForeignKey("JobReq", on_delete=models.CASCADE, related_name='form_of_work_links', db_column='jobReqId')
    form_of_work = models.ForeignKey("FormOfWork", on_delete=models.CASCADE, related_name='job_req_form_of_work_links', db_column='formOfWorkId')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'JobReqFormOfWork'
        unique_together = ('job_req', 'form_of_work')
