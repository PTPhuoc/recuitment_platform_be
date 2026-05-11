from django.db import models
from django_ulidfield import ULIDField

class Industry(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    slug = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'Industry'