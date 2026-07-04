from django.db import models
from django_ulidfield import ULIDField

class FormOfWork(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    slug = models.CharField(db_index=True, max_length=100, unique=True)
    status = models.CharField(
        max_length=10,
        choices=(("active", "Active"), ("delete", "Delete")),
        default="active",
        db_index=True,
    )
    date_created = models.DateTimeField(auto_now_add=True, db_column='dateCreated')
    date_deleted = models.DateTimeField(null=True, blank=True, db_column='dateDeleted')

    class Meta:
        db_table = 'FormOfWork'