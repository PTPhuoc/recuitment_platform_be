from django.db import models
from django_ulidfield import ULIDField


# models/CompanyLocation.py
class CompanyLocation(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='company_locations', db_column='companyId')
    location = models.ForeignKey('Locations', on_delete=models.CASCADE, related_name='location_companies', db_column='locationId')
    detail_address = models.CharField(db_column='detailAddress', max_length=255, blank=True, null=True)
    date_create = models.DateField(db_column='dateCreate', blank=True, null=True)

    class Meta:
        db_table = 'CompanyLocation'
        unique_together = ('company', 'location')
