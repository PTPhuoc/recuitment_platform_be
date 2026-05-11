from django.db import models
from django_ulidfield import ULIDField

class Education(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    slug = models.CharField(max_length=100, db_index=True)

    class Meta:
        db_table = 'Education'