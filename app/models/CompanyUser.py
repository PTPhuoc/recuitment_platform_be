from django.db import models
from django_ulidfield import ULIDField

from app.models import Employer, Company


class CompanyUser(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE, db_column='employerId',
                                       related_name='company_user')
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='companyId',
                                      related_name='company_user')
    role = models.CharField(max_length=20, default="pending")
    status = models.CharField(max_length=20, default="pending")
    date_created = models.DateTimeField(auto_now_add=True, db_column='dateCreated')

    class Meta:
        db_table = 'CompanyUser'
        unique_together = ('employer_id', 'company_id')
