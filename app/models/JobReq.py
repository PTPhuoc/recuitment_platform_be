from django.db import models
from django_ulidfield import ULIDField


class JobReq(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    job = models.OneToOneField("Job", on_delete=models.CASCADE, related_name='require', db_column='jobId')
    form_of_work = models.ManyToManyField("FormOfWork", through="JobReqFormOfWork", related_name='job_req_form_of_work')
    location = models.ForeignKey("Locations", on_delete=models.SET_NULL, null=True, blank=True, related_name='req_location', db_column='locationId')
    quantity = models.IntegerField(default=0)
    industries = models.ManyToManyField("Industry", through="JobReqIndustry", related_name='job_req_industries')
    educations = models.ManyToManyField("Education", through="JobReqEducation", related_name='job_req_educations')
    job_level = models.ManyToManyField("JobLevel", through="JobReqJobLevel", related_name='job_req_job_level')
    max_salary = models.IntegerField(default=0)
    min_salary = models.IntegerField(default=0)
    max_experience = models.IntegerField(default=0)
    min_experience = models.IntegerField(default=0)

    class Meta:
        db_table = 'JobReq'