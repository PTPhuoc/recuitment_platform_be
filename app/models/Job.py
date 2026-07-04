from django.db import models
from django_ulidfield import ULIDField
from app.models import Company


class Job(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job', db_column='companyId')
    name = models.CharField(max_length=255)
    source_link = models.TextField(null=True, db_index=True, db_column='sourceLink')
    description = models.TextField(null=True)
    status = models.CharField(
        max_length=20,
        choices=(("pending", "Pending"),
                 ("active", "Active"),
                 ("ban", "Ban"),
                 ("delete", "Delete")),
        default='pending',
        db_index=True)
    date_deleted = models.DateTimeField(null=True, default=None, blank=True, db_column='dateDeleted')
    date_created = models.DateTimeField(auto_now_add=True, db_column='dateCreated')
    date_limited = models.DateTimeField(null=False, db_column='dateLimited')

    class Meta:
        db_table = 'Job'
