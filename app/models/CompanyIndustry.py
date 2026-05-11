from django.db import models
from django_ulidfield import ULIDField


# models/CompanyIndustry.py
class CompanyIndustry(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='company_industries', db_column='companyId')
    industry = models.ForeignKey('Industry', on_delete=models.CASCADE, related_name='industry_companies', db_column='industryId')
    date_create = models.DateTimeField(auto_now_add=True, db_index=True, db_column='dateCreate')

    class Meta:
        db_table = 'CompanyIndustry'
        unique_together = ('company', 'industry')