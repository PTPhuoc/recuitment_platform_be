from django.db import models
from django_ulidfield import ULIDField

class FormOfWork(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    slug = models.CharField(db_index=True, max_length=100, unique=True)

    class Meta:
        db_table = 'FormOfWork'